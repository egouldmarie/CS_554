
LPAR = "lpar"
RPAR = "rpar"
LBRAC = "lbrac"
RBRAC = "rbrac"
INT   = "int"
VAR   = "var"
ASSIGN = "assign"
SEQ    = "sequencing"
OP_A   = "op_a"
OP_R   = "op_r"
NEWL   = "newline"
IGN    = "ignore"
MISM   = "mismatch"
MULT   = "mult"
ADD    = "add"
SUB    = "sub"

class Parser:
    '''
    Define and establish methods for a parser of a sequence of tokens
    produced by a separate scanner or lexer. Parser(tokens) takes as
    input a sequence of Token objects, each consisting of a length-4
    NamedTuple of the form (type, value, line, column) and returns ...
    an abstract syntax tree, by consuming the tokens one by one and
    using recursive functions to match the tokens against grammar rules.

    CURRENTLY: Parser can handle simple mathematical expressions
    and a sequence of simple assignment statements.
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
        For a sum or difference expression such as x + 2 * y.
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

    def parse(self):
        '''
        Top-level method to start the parsing process, assuming a list
        of tokens associated with a program consisting of a sequence
        of statements.
        '''
        while self.current_token_index < len(self.tokens):
            self.program_ast.append(self.statement())
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
