
# ================= #
# Useful constants  #
# ================= #

LPAR   = "lpar"
RPAR   = "rpar"
LBRAC  = "lbrac"
RBRAC  = "rbrac"
INT    = "int"
VAR    = "var"
ASSIGN = "assign"
SKIP   = "skip"
SEQ    = "sequencing"
OP_A   = "op_a"
OP_R   = "op_r"
NEWL   = "newline"
IGN    = "ignore"
MISM   = "mismatch"
MULT   = "mult"
ADD    = "add"
SUB    = "sub"
IF     = "if"
THEN   = "then"
ELSE   = "else"
FI     = "fi"
WHILE  = "while"
DO     = "do"
OD     = "od"
NOT    = "not"
AND    = "and"
OR     = "or"
TRUE   = "true"
FALSE  = "false"

class Parser:
    '''
    Define and establish methods for a parser of a sequence of tokens
    produced by a separate scanner or lexer. Parser(tokens) takes as
    input a sequence of Token objects, each consisting of a length-4
    NamedTuple of the form (type, value, line, column) and returns ...
    an abstract syntax tree, by consuming the tokens one by one and
    using recursive functions to match the tokens against grammar rules.
    '''

    def __init__(self, tokens):
        self.stack = []
        self.tokens = tokens
        self.current_pos = 0
        self.current_token_index = 0
        self.current_token = self.tokens[0] if self.tokens else None
        # At the top level, the program AST will be a list of
        # statements, each statement being a collection of nested
        # tuples (essentially sub-trees).
        self.program_ast = []
        self.error_count = 0 # for some debugging control

    def _advance(self):
        self.current_token_index += 1
        if self.current_token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token_index]
        else:
            self.current_token = None

    def consume(self, expected_type):
        '''
        If the current token (as found in self.current_token) matches
        the expected_type, consume the token and advance to the next
        token by calling the _advance() helper fxn.
        '''
        if self.current_pos >= len(self.tokens):
            raise SyntaxError("Unexpected end of input.")
        token = self.current_token
        if token.type == expected_type:
            # self.current_pos += 1
            self._advance()
            return token
        else:
            raise SyntaxError(
                    f"In Parser.consume(), expected token type "
                    f"{expected_type} but got {token.type} on "
                    f"line {token.line}.")

    def peek(self, expected_type):
        '''
        Check the type of the current token without consuming it,
        comparing it to the expected_type; this can be important for
        context-checking.
        '''
        if self.current_token_index < len(self.tokens):
            return self.current_token.type == expected_type
        return False

    def peek_ahead(self, expected_type):
        '''
        Check the next token (i.e. the upcoming token after the current
        one) without consuming it, comparing it to the expected_type.
        Used for context checking.
        '''
        if self.current_token_index < (len(self.tokens) - 1):
            return (self.tokens[self.current_token_index + 1].type
                    == expected_type)
        return False

    def parse(self):
        '''
        Top-level method to start the parsing process, assuming a list
        of tokens associated with a program consisting of a sequence
        of statements.
        '''

        # begin with the very first statement
        _stmt = self.statement()
        if _stmt:
            if _stmt != (SKIP):
                self.program_ast.append(_stmt)
        else:
            _last_token = self.tokens[self.current_token_index]
            _value = _last_token.value
            _line = _last_token.line
            raise SyntaxError(
                    "Parser.statement() method encountered a problematic "
                    f"statement on line {_line}. Last token processed "
                    f"was '{_value}' on line {_line}.")

        # then if statement(s) followed by ';', keep processing
        while self.peek(SEQ):
            self.consume(SEQ)
            _stmt = self.statement()
            if _stmt:
                if _stmt != (SKIP):
                    self.program_ast.append(_stmt)
            else:
                raise SyntaxError(
                    "Parser.statement() discovered a missing or "
                    f"problematic statement on line {_line}. "
                    "Last token processed "
                    f"was '{_value}' on line {_line}."
                )
        if self.current_token_index < len(self.tokens) - 1:
            # parsing ended prematurely, possibly due to an
            # unexpected token or a missing sequencing token ';'
            _last_token = self.tokens[self.current_token_index]
            _value = _last_token.value
            _line = _last_token.line
            raise SyntaxError(
                    "Parsing ended prematurely, possibly due to an "
                    "unexpected token or missing seq token ';'. "
                    "Last token processed was "
                    f"'{_value}' on line {_line}.")
            
        return self.program_ast

    def statement(self):
        '''
        Pursue different parsing method(s) based on current statement
        (or what the project details call a 'command').
        '''
        if self.current_token is None:
            # possibly consumed all code while expecting more
            # e.g. when a seq of commands incorrectly ends with ';'
            _prev_token = self.tokens[self.current_token_index-1]
            _value = _prev_token.value
            _line  = _prev_token.line
            raise SyntaxError(
                "Token expected but None found. "
                " Last token successfully processed "
                f"was '{_value}' on line {_line}. "
                "Possible extra ';' token?"
            )
        
        # assignment (e.g., x := 3 + 2 * y)
        if self.current_token.type == VAR and self.peek_ahead(ASSIGN):
            return self.parse_assignment_stmt()
        
        # skip (e.g., if x > 0 then x := x + 1 else skip)
        if self.peek(SKIP):
            return self.parse_skip_stmt()
        
        # if-then-else
        if self.current_token.type == IF:
            return self.parse_if_stmt()
        
        # while-do
        if self.peek(WHILE):
            return self.parse_while_stmt()

    def parse_assignment_stmt(self):
        '''
        Parsing assignment statements of the form x := expr .
        Method assumes caller has already verified that the statement
        to be parsed is indeed an assignment statement.
        '''
        var_token = self.consume(VAR)
        assign_token = self.consume(ASSIGN)
        right = self.expr()
        result = (ASSIGN, (VAR, var_token.value), right)
        return result
    
    def parse_skip_stmt(self):
        '''
        Parsing of 'skip' statements, which might appear (e.g.) in
        the else block of an IF statement like this:
            if x > 0 then
              x := x + 1
            else
              skip
            fi;
        A skip statement does nothing and can generally be ignored
        or even eliminated from the parse tree.
        '''
        self.consume(SKIP)   # discard 'skip' token

        # we could choose something else here;
        # None will be confused with some errors elsewhere, so we
        # return (SKIP) and let local caller fxns decide what to do
        # with a SKIP (typically ignore it).
        return (SKIP)
    
    def parse_if_stmt(self):
        '''
        Parsing of if-then-else statements like this:
            if x > 0 then
              x := x + 1;
              y := true
            else
              x := 0
            fi
        where the 'else' block could be a simple 'skip' command.
        Method assumes caller has already verified that the statement
        to be parsed is indeed an if-then-else statement.
        '''

        self.consume(IF)               # discard 'if'
        condition = self.bool_expr()   # recursively parse bool cond
        self.consume(THEN)             # discard 'then'

        # fixing true_block to deal correctly with SEQ issues
        true_block = []
        # true block of statements might be empty
        _stmt = self.statement() # check what this returns?
        # NEED to deal with possible None for _stmt below:
        if _stmt and _stmt != (SKIP):
            true_block.append(_stmt)
        while self.peek(SEQ):
            self.consume(SEQ)
            _stmt = self.statement()
            if _stmt != (SKIP):
                if _stmt:
                    true_block.append(_stmt)
                else:
                    # scanner may catch all these errors
                    raise SyntaxError("Extra ';' detected in true_block!")
        
        self.consume(ELSE)             # discard 'else'

        else_block = []
        # else block of statements might be empty
        # needs to be improved still (see elsewhere for examples)
        _stmt = self.statement()
        if _stmt and _stmt != (SKIP):
            else_block.append(_stmt)
        while self.peek(SEQ):
            self.consume(SEQ)
            _stmt = self.statement()
            if _stmt != (SKIP):
                if _stmt:
                    else_block.append(_stmt)
                else:
                    # scanner may catch all these errors
                    raise SyntaxError("Extra ';' detected!")
            
        self.consume(FI)               # discard 'fi'

        # note that the true_block and/or while_block can be empty
        return (IF, condition, true_block, else_block)

    def parse_while_stmt(self):
        '''
        Parsing of while loops like this:
            while x > 0 do
              x := x - 1;
              y := y + 1
            od
        Method assumes caller has already verified that the
        statement to be parsed is indeed a while-do statement.
        '''

        self.consume(WHILE)            # discard 'while'
        condition = self.bool_expr()   # recursively parse bool cond
        self.consume(DO)               # discard 'do'

        while_block = []
        # while block might be empty
        _stmt = self.statement()
        if _stmt and _stmt != (SKIP):
            while_block.append(_stmt)
        
        while self.peek(SEQ):
            self.consume(SEQ)
            _stmt = self.statement()
            if _stmt != (SKIP):
                if _stmt:
                    while_block.append(_stmt)
                else:
                    # scanner may catch all these errors
                    raise SyntaxError("Extra ';' detected!")
        self.consume(OD)               # discard 'od'

        # note that it's possible to empty while_block
        return (WHILE, condition, while_block)
    
    def expr(self):
        '''
        Handles either an arithmetic expression (e.g. x + 2 * y)
        or a boolean expression (e.g. x >= y).
        '''
        # distinguish boolean vs arithmetic expressions
        if (self.current_token.type in [LBRAC, NOT, AND, OR]):
            result = self.bool_expr()
        else:
            result = self.arith_expr()
        return result
    
    # ====================================== #
    # arithmetic expressions and components  #
    # SEE: arith_expr, term, factor          #
    # ====================================== #
    
    def arith_expr(self):
        '''
        For a sum or difference expression such as x + 2 * y (which
        then consists of arithmetic terms and factors).
        '''
        result = self.term()
        while (self.current_token
               and (self.current_token.value in ['+', '-'])):
            op_token = self.current_token
            if op_token.value == '+':
                self.consume(OP_A)
                right = self.term()
                result = (ADD, result, right)
            else:
                # subtraction expression
                self.consume(OP_A)
                right = self.term()
                result = (SUB, result, right)

        return result
    
    def term(self):
        '''
        For a participant (term) in a sum or difference expression.
        For example, in the expression 'x + 2 * y,'
        the 'x' and the '2 * y' are both terms.
        '''
        result = self.factor()
        while (self.current_token and self.current_token.value == '*'):
            op_token = self.consume(OP_A)
            right = self.factor()
            result = (MULT, result, right)
        return result
    
    def factor(self):
        '''
        For a participant in a multiplication, such a participant being
        a number, a variable, or a parenthesized expression.
        '''
        if self.peek(INT):
            token = self.consume(INT)
            return (INT, int(token.value))
        elif self.peek(VAR):
            token = self.consume(VAR)
            return (VAR, token.value)
        elif self.peek(LPAR):
            self.consume(LPAR)    # consume and discard '('
            result = self.expr()  # recursively parse inner expr
            self.consume(RPAR)    # consume and discard ')'
            return result
        else:
            _value = self.current_token.value
            _line  = self.current_token.line
            raise SyntaxError(
                    "In Parser.factor(), encountered unexpected token "
                    f"'{_value}' on line {_line}.")
    
    # ====================================== #
    # boolean expressions and components     #
    # SEE: bool_expr, bool_term, bool_factor #
    # ====================================== #
    
    def bool_expr(self):
        '''
        Primarily for a boolean OR, which has the lowest precedence
        in the precedence order [] > NOT > AND > OR.
        b1 OR b2 is analogous to arithmetic expression;
        b1 AND b2 is analogous to arithmetic term;
        NOT[b], [b] are analogous to arithmetic factor.
        '''
        result = self.bool_term()
        if (self.current_token
               and (self.current_token.value == OR)):
            self.consume(OR)
            right = self.bool_term()
            result = (OR, result, right)
        return result
    
    def bool_term(self):
        '''
        For a boolean AND, whose components then might themselves be
        bool_expr, bool_term, or bool_factor.
        '''
        result = self.bool_factor()
        while (self.current_token and self.peek(AND)):
            self.consume(AND)
            right = self.bool_factor()
            result = (AND, result, right)
        return result
    
    def bool_factor(self):
        '''
        For parsing a boolean of the form [b] (i.e. a boolean in
        square brackets) or a NOT[b]. Such a factor might be an
        element of a bool_term (an AND) or a bool_expr (an OR), and
        the b itself might then be a bool_expr, bool_term, or
        bool_factor.
        '''
        if self.peek(NOT):
            self.consume(NOT)
            self.consume(LBRAC)        # discard [
            result = self.bool_expr()  # recursively parse inner expr
            self.consume(RBRAC)        # discard ]
            return (NOT, result)
        elif self.peek(LBRAC):
            self.consume(LBRAC)        # discard [
            result = self.bool_expr()  # recursively parse inner expr
            self.consume(RBRAC)        # discard ]
            return result
        elif self.peek(TRUE):
            self.consume(TRUE)
            return TRUE
        elif self.peek(FALSE):
            self.consume(FALSE)
            return FALSE
        else:
            # we must have a relational expression such as x < y
            left = self.arith_expr()
            op = self.consume(OP_R).value
            right = self.arith_expr()
            result = (op, left, right)
            return result

################################################################################
# type flags
l_types = {
    "false":        "0",
    "true":         "1",
    "not":          "!",
    "and":          "&",
    "or":           "|",
    "skip":         "%",
    "if":           "<",
    "then":         "?",
    "else":         ":",
    "fi":           ">",
    "while":        "w",
    "do":           "\\",
    "od":           "/",
    "int":          "n",
    "var":          "x",
    "op_a":         "^",
    "op_r":         "r",
    "assign":       "=",
    "sequencing":   ";",
    "lpar":         "(",
    "rpar":         ")",
    "lbrac":        "[",
    "rbrac":        "]",
}

class PDA:
    def __init__(self, input):
        self.input = input

        self.states = []
        self.stack = []
        self.rules = []

def parseTokens(tokens):
    input = " ".join([l_types[t.type] for t in tokens])
    input = "'"+input+"'"
    print(input)
