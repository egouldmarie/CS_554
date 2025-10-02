
class TokenType:
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

class Parser:
    '''
    Define and establish methods for a parser of a sequence of tokens
    produced by a separate scanner or lexer. Parser(tokens) takes as
    input a sequence of Token objects, each consisting of a length-4
    NamedTuple of the form (type, value, line, column) and returns ...
    an abstract syntax tree, by consuming the ntokens one by one and
    using recursive functions to match the tokens against grammar rules.

    ! RIGHT NOW: JUST modeled on parsing for simple math expressions. !
    '''

    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[0] if self.tokens else None
    
    def _advance(self):
        self.current_token_index += 1
        self.current_token = self.tokens[self.current_token_index]

    def _eat(self, token_type):
        if self.current_token and self.current_token.type == token_type:
            self._advance()
        else:
            raise Exception(
                    f"Expected token type {token_type} but got "
                    f"{self.current_token.type if self.current_token else 'EOF'}")

    def factor(self):
        token = self.current_token
        if token.type == INT:
            self._eat(INT)
            return int(token.value)
        # elif token.type == BLAH BLAH BLAH
        # else raise Exception(), etc

    def term(self):
        result = self.factor()
        while (self.current_token
               and self.current_token_index.type == OP_A):
            

        pass

    def expr(self):
        result = self.term()
        pass

    def parse(self):
        if not self.tokens:
            return None
        return self.expr()
    
