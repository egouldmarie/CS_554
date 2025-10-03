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
    '''

    def __init__(self, tokens):
        self.tokens = tokens
        self.current_pos = 0
        self.current_token_index = 0
        self.current_token = self.tokens[0] if self.tokens else None

    # COME BACK TO THIS; can be a nice modularization
    def _advance(self):
        self.current_token_index += 1
        if self.current_token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token_index]
        else:
            self.current_token = None
    
    def consume(self, expected_type):
        '''
        Consume the next token if it matches the expected token type.
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
        Check the next token without consuming it, comparing it to the
        expected_type; this can be important for context-checking.
        '''
        if self.current_token_index < len(self.tokens):
            return self.current_token.type == expected_type
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
        Start the parsing process.
        '''
        parse_tree = self.expr()
        if self.current_token_index < len(self.tokens):
            raise SyntaxError(
                    "Parsing interrupted; failed to parse all tokens. "
                    f"Last token parsed was: "
                    f"{self.tokens[self.current_token_index - 1]}."
            )
        return parse_tree


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

    parser = Parser(tokens)
    parse_tree = parser.parse()
    print(f"parse_tree: {parse_tree}")

    print("-------------------------------------------------------------------")
    
    print("\n")


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