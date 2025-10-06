
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

    CURRENTLY: Parser can handle simple mathematical and boolean
    expressions, and a sequence of simple assignment statements
    (including boolean assignments).
    Does NOT yet handle other statements/commands.
    '''

    def __init__(self, tokens):
        self.stack = []
        self.tokens = tokens
        self.current_pos = 0
        self.current_token_index = 0
        self.current_token = self.tokens[0] if self.tokens else None
        # At the top level, the program AST will be a list of
        # statements, each of which will then have its own sub-AST
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
                    f"{expected_type} but got {token.type}.")

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
            self.consume(LPAR)    # without using returned token
            result = self.expr()  # recursively parse inner expr
            self.consume(RPAR)    # without using returned token
            return result
        else:
            raise SyntaxError(
                    f"Unexpected token found in Parser.factor(): "
                    f"{self.current_token.value}.")

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

    def expr(self):
        '''
        Handles either an arithmetic expression (e.g. x + 2 * y)
        or a boolean expression (e.g. x >= y).
        '''
        # ditinguish boolean vs arithmetic expressions
        if (self.current_token.type in [LBRAC, NOT, AND, OR]):
        # if (self.peek(LBRAC) or self.peek(NOT) 
        #     or self.peek_ahead(AND) or self.peek_ahead(OR)):
            print(f"Found boolean expression beginning with: {self.current_token.value}")
            result = self.bool_expr()
        else:
            result = self.arith_expr()
        return result
    
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
    
    def bool_expr(self):
        '''
        Primarily for a boolean OR, which has the lowest precedence
        in the precedence order [] > NOT > AND > OR.
        b1 OR b2 is analogous to arithmetic expression;
        b1 AND b2 is analogous to arithmetic term;
        NOT[b], [b] are analogous to arithmetic factor.
        '''
        print(f"Entering bool_expr() with: ")
        print(f"    current_token = {self.current_token}")
        result = self.bool_term()
        if (self.current_token
               and (self.current_token.value == OR)):
            self.consume(OR)
            right = self.bool_term()
            result = (OR, result, right)
        print(f"About to exit bool_expr() with: ")
        print(f"    result = {result}")
        return result
    
    def bool_term(self):
        '''
        For a boolean AND, whose components then might themselves be
        bool_expr, bool_term, or bool_factor.
        '''
        print(f"Entering bool_term() with: ")
        print(f"    current_token = {self.current_token}")
        result = self.bool_factor()
        while (self.current_token and self.peek(AND)):
            self.consume(AND)
            right = self.bool_factor()
            result = (AND, result, right)
        print(f"About to exit bool_term() with: ")
        print(f"    result = {result}")
        return result
    
    def bool_factor(self):
        '''
        For parsing a boolean of the form [b] (i.e. a boolean in
        square brackets) or a NOT[b]. Such a factor might be an
        element of a bool_term (an AND) or a bool_expr (an OR), and
        the b itself might then be a bool_expr, bool_term, or
        bool_factor.
        '''
        print(f"Entering bool_factor() with: ")
        print(f"    current_token = {self.current_token}")
        # if self.peek(VAR):
        #     # we might have something like x < y
        #     token = self.consume(VAR)
        #     return (VAR, token.value)
        if self.peek(NOT):
            self.consume(NOT)
            self.consume(LBRAC)        # discard [
            result = self.bool_expr()  # recursively parse inner expr
            self.consume(RBRAC)        # discard ]
            print(f"About to exit bool_factor() with: ")
            print(f"    result = {result}")
            return (NOT, result)
        elif self.peek(LBRAC):
            self.consume(LBRAC)        # discard [
            result = self.bool_expr()  # recursively parse inner expr
            self.consume(RBRAC)        # discard ]
            print(f"About to exit bool_factor() with: ")
            print(f"    result = {result}")
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
            print(f"About to exit bool_factor() with: ")
            print(f"    result = {result}")
            return result

    def parse(self):
        '''
        Top-level method to start the parsing process, assuming a list
        of tokens associated with a program consisting of a sequence
        of statements.
        '''
        while self.current_token_index < len(self.tokens):
            _stmt = self.statement()
            if _stmt is not None:
                self.program_ast.append(_stmt)
        return self.program_ast

        # ======================================================== #
        # Previous code below when dealing only with expressions
        # see above dev for dealing with sequence of statements.
        # Leaving this here for a while for a reminder.
        # ======================================================== #
        # parse_tree = self.expr()
        # if self.current_token_index < len(self.tokens):
        #     raise SyntaxError(
        #             "Parsing interrupted; failed to parse all tokens. "
        #             f"Last token parsed was: "
        #             f"{self.tokens[self.current_token_index - 1]}."
        #     )
        # return parse_tree

    def statement(self):
        '''
        Pursue different parsing method(s) based on current statement
        (or what the project details call a 'command').
        '''
        # assignment (e.g., x := 3 + 2 * y)
        if self.current_token.type == VAR and self.peek_ahead(ASSIGN):
            return self.parse_assignment_stmt()
        
        # skip (e.g., if x > 0 then x := x + 1 else skip)
        if self.peek(SKIP):
            print(f"FOUND a skip statement!")
            return self.parse_skip_stmt()
        
        # if-then-else
        if self.current_token.type == IF:
            return self.parse_if_stmt()

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
        if self.peek(SEQ):
            # we check b/c the last statement in a program might
            # not end with a sequence (;) marker
            self.consume(SEQ)
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
        print("Entering parse_skip_stmt() method. ")
        self.consume(SKIP)   # discard 'skip' token
        if self.peek(SEQ):
            # we check b/c the last statement in a program might
            # not end with a sequence (;) marker
            self.consume(SEQ)

        # we could choose something else here;
        # None will prompt a statement accumulator to ignore.
        return None
    
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

        true_block = []
        while (self.current_token_index < len(self.tokens)
               and self.current_token.type != ELSE):
            _stmt = self.statement()
            if (_stmt is not None):
                true_block.append(_stmt)
        self.consume(ELSE)             # discard 'else'

        else_block = []
        while (self.current_token_index < len(self.tokens)
               and self.current_token.type != FI):
            _stmt = self.statement()
            if (_stmt is not None):
                else_block.append(_stmt)
        self.consume(FI)               # discard 'fi'

        if self.peek(SEQ):
            # if-then-else will typically end with ';' marker, but
            # doesn't have to if it is the last statement in the
            # program or in a block
            self.consume(SEQ)

        if len(else_block) != 0:
            return (IF, true_block, else_block)
        else:
            return (IF, true_block)

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
