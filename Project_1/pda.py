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
################################################################################

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

A = 'a'
B = 'b'
C = 'c'
EVAL = 'Eval'
DONE = 'Done'
ERROR = 'Error'

class PDA:
    def __init__(self, tokens):
        self.tokens = tokens
        self.stack = [C]
        self.current_state = EVAL
        self.pointer = 0

    def getNext(self):
        try:
            self.input = self.tokens[self.pointer].type
            self.value = self.tokens[self.pointer].value
        except:
            self.input = None
            self.value = None

        self.pointer = self.pointer+1

    def step(self):
        self.getNext()
        input = self.input
        print("Step:", self.pointer)
        print("Stack:", self.stack)
        print("Input:", input, self.value)

        match self.current_state:
            case 'Eval':
                match input:
                    # evaluating command c
                    case 'var':
                        pop = (self.stack and self.stack.pop())
                        if pop == C:
                            self.stack.append(ASSIGN)
                        elif pop == B:
                            self.stack.append(OP_R)
                        elif pop != A:
                            self.current_state = ERROR
                    case 'int':
                        pop = (self.stack and self.stack.pop())
                        if pop == B:
                            self.stack.append(OP_R)
                        elif pop != A:
                            self.current_state = ERROR
                    case 'skip':
                        if (self.stack and self.stack.pop()) != C:
                            self.current_state = ERROR
                    case 'sequencing':
                        self.stack.append(C)
                    case 'assign':
                        if (self.stack and self.stack.pop()) == ASSIGN:
                            self.stack.append(A)
                        else:
                            self.current_state = ERROR
                    case 'if':
                        if (self.stack and self.stack.pop()) == C:
                            self.stack.append(IF)
                            self.stack.append(B)
                        else:
                            self.current_state = ERROR
                    case 'then':
                        if (self.stack and self.stack.pop()) == IF:
                            self.stack.append(THEN)
                            self.stack.append(C)
                        else:
                            self.current_state = ERROR
                    case 'else':
                        if (self.stack and self.stack.pop()) == THEN:
                            self.stack.append(ELSE)
                            self.stack.append(C)
                        else:
                            self.current_state = ERROR
                    case 'fi':
                        if (self.stack and self.stack.pop()) != ELSE:
                            self.current_state = ERROR
                    case 'while':
                        if (self.stack and self.stack.pop()) == C:
                            self.stack.append(WHILE)
                            self.stack.append(B)
                        else:
                            self.current_state = ERROR
                    case 'do':
                        if (self.stack and self.stack.pop()) == WHILE:
                            self.stack.append(DO)
                            self.stack.append(C)
                        else:
                            self.current_state = ERROR
                    case 'od':
                        if (self.stack and self.stack.pop()) != DO:
                            self.current_state = ERROR
                    case 'true':
                        if (self.stack and self.stack.pop()) != B:
                            self.current_state = ERROR
                    case 'false':
                        if (self.stack and self.stack.pop()) != B:
                            self.current_state = ERROR
                    case 'and':
                        self.stack.append(B)
                    case 'or':
                        self.stack.append(B)
                    case 'not':
                        if (self.stack and self.stack.pop()) == B:
                            self.stack.append(NOT)
                        else:
                            self.current_state = ERROR
                    case 'lbrac':
                        pop = (self.stack and self.stack.pop())
                        if pop == NOT or pop == B:
                            self.stack.append(LBRAC)
                            self.stack.append(B)
                        else:
                            self.current_state = ERROR
                    case 'rbrac':
                        if (self.stack and self.stack.pop()) != LBRAC:
                            self.current_state = ERROR
                    case 'lpar':
                        pop = (self.stack and self.stack.pop())
                        if pop == B:
                            self.stack.append(OP_R)
                            self.stack.append(LPAR)
                            self.stack.append(A)
                        elif pop == A:
                            self.stack.append(LPAR)
                            self.stack.append(A)
                        else:
                            self.current_state = ERROR
                    case 'rpar':
                        if (self.stack and self.stack.pop()) != LPAR:
                            self.current_state = ERROR
                    case 'op_a':
                        self.stack.append(A)
                    case 'op_r':
                        if (self.stack and self.stack.pop()) == OP_R:
                            self.stack.append(A)
                        else:
                            self.current_state = ERROR
                    # go to DONE state
                    case None:
                        # end of input
                        if (self.stack and self.stack.pop()):
                            # there should not be anything left in the stack
                            self.current_state = ERROR
                        else:
                            self.current_state = DONE
                    # otherwise go to ERROR state
                    case _:
                        self.current_state = ERROR
            case 'Done':
                print("Success!")
            case 'Error':
                print("Error parsing program")

def parseTokens(tokens):
    print("Number of tokens:", len(tokens))
    pda = PDA(tokens)

    while (pda.current_state!=ERROR and pda.current_state!=DONE):
        pda.step()
        print("State:", pda.current_state.upper())
    if pda.current_state==ERROR:
        print("Error")
    elif pda.current_state==DONE:
        print("Success!")
    else:
        print("We should not be in this state:", pda.current_state)