import sys
from scanner import tokenize

# class TokenType:
#     LPAR = "lpar"
#     RPAR = "rpar"
#     LBRAC = "lbrac"
#     RBRAC = "rbrac"
#     INT   = "int"
#     VAR   = "var"
#     ASSIGN = "assign"
#     SEQ    = "sequencing"
#     OP_A   = "op_a"
#     OP_R   = "op_r"
#     NEWL   = "newline"
#     IGN    = "ignore"
#     MISM   = "mismatch"

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

    ! RIGHT NOW: JUST coding for parsing for simple math expressions
    of the form x + 2 * y, etc. !

    ! WORKING ON EXTENDING to handle a sequence (SEQ) of statements,
    starting with simple assignment statements.
    '''

    def __init__(self, tokens):
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

    # def _eat(self, token_type):
    #     if self.current_token and self.current_token.type == token_type:
    #         self._advance()
    #     else:
    #         raise Exception(
    #                 f"Expected token type {token_type} but got "
    #                 f"{self.current_token.type if self.current_token else 'None'}")

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
            self.consume(LPAR)    # without using return token
            result = self.expr()  # recursively parse inner expr
            self.consume(RPAR)
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
        For a sum or difference expression such as x + 2*y.
        '''
        result = self.term()
        while (self.current_token and (self.current_token.value == '+'
               or self.current_token.value == '-')):
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
        # print("Entering parse() method, with: ")
        # print(f"    self.current_token = {self.current_token}")
        # print(f"    self.current_token_index = {self.current_token_index}")
        # print(f"    self.peek_ahead(ASSIGN) = {self.peek_ahead(ASSIGN)}")
        while self.current_token_index < len(self.tokens):
            self.program_ast.append(self.statement())
        return self.program_ast

        # ======================================================== #
        # previous code below when dealing only with expressions
        # see above dev for dealing with sequence of statements
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
        # if self.error_count < 4:
        #     self.error_count += 1
        #     print(f"\nEntering statement() method with:")
        #     print(f"    self.current_token.type = {self.current_token.type}")
        #     print(f"    self.peek_ahead(ASSIGN) = {self.peek_ahead(ASSIGN)}")
        # assignment
        if self.current_token.type == VAR and self.peek_ahead(ASSIGN):
            return self.parse_assignment_stmt()
    
    def parse_assignment_stmt(self):
        '''
        For assignment statements of the form x := expr .
        '''
        # print("\nEntering parse_assignment_stmt().")
        var_token = self.consume(VAR)
        # print(f"    consumed VAR token with value {var_token.value}")
        assign_token = self.consume(ASSIGN)
        # print(f"    consumed ASSIGN token with value {assign_token.value}")
        right = self.expr()
        # print("    finished self.expr()")
        result = (ASSIGN, (VAR, var_token.value), right)
        if self.peek(SEQ):
            self.consume(SEQ)
        return result


if __name__ == "__main__":

    print("-------------------------------------------------------------------")

    # read in file text
    with open(sys.argv[1], 'r') as file:
        text = file.read()

    print("\nInput text:")
    print("-------------------------------------------------------------------")
    print(text)
    print("-------------------------------------------------------------------")
    print("Generated tokens:\n")

    tokens = []
    for token in tokenize(text):
        print(token)
        tokens.append(token)
    
    print("-------------------------------------------------------------------")
    print("Initializing Parser ...")
    parser = Parser(tokens)
    print("Starting Parser .......")
    parse_tree = parser.parse()
    print(f"parse_tree: {parse_tree}")

    print("-------------------------------------------------------------------")
    
    print("\n")
