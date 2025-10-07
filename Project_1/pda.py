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

EPSILON = -1
NOPOP = "_"
A = 'a'
B = 'b'
C = 'c'
DONE = 'Done'
ERROR = 'Error'

class PDA:
    def __init__(self, tokens):
        self.tokens = tokens
        self.stack = [C]
        self.current_state = C
        self.count = 1

    def getNext(self):
        self.input = (self.tokens and self.tokens.data) or -1
        self.value = (self.tokens and self.tokens.value) or -1
        if (self.tokens and self.tokens.next):
            self.tokens = self.tokens.next
        else:
            self.tokens = None

    def step(self):
        self.getNext()
        input = self.input
        print("Step:", self.count)
        print("Stack:", self.stack)
        print("Input:", input, self.value)

        self.count = self.count+1

        match self.current_state:
            case 'c':
                match input:
                    # stay in state C
                    case 'var':
                        if (self.stack and self.stack.pop()) == C:
                            self.stack.append(ASSIGN)
                        else:
                            self.current_state = ERROR
                    case 'skip':
                        if (self.stack and self.stack.pop()) != C:
                            self.current_state = ERROR
                    case 'sequencing':
                        self.stack.append(C)
                    case 'else':
                        if (self.stack and self.stack.pop()) == THEN:
                            self.stack.append(ELSE)
                            self.stack.append(C)
                        else:
                            self.current_state = ERROR
                    case 'fi':
                        if (self.stack and self.stack.pop()) != ELSE:
                            self.current_state = ERROR
                    case 'od':
                        if (self.stack and self.stack.pop()) != DO:
                            self.current_state = ERROR
                    # go to state A
                    case 'assign':
                        if (self.stack and self.stack.pop()) == ASSIGN:
                            self.stack.append(A)
                            self.current_state = A
                        else:
                            self.current_state = ERROR
                    # go to state B
                    case 'if':
                        if (self.stack and self.stack.pop()) == C:
                            self.stack.append(IF)
                            self.stack.append(B)
                            self.current_state = B
                        else:
                            self.current_state = ERROR
                    case 'while':
                        if (self.stack and self.stack.pop()) == C:
                            self.stack.append(WHILE)
                            self.stack.append(B)
                            self.current_state = B
                        else:
                            self.current_state = ERROR
                    # go to DONE state
                    case -1:
                        if (self.stack and self.stack.pop()):
                            self.current_state = ERROR
                        else:
                            self.current_state = DONE
                    case _:
                        self.current_state = ERROR
            case 'b':
                match input:
                    # stay in state B
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
                    # go to state A
                    case 'var':
                        if (self.stack and self.stack.pop()) == B:
                            self.stack.append(OP_R)
                            self.current_state = A
                        else:
                            self.current_state = ERROR
                    case 'int':
                        if (self.stack and self.stack.pop()) == B:
                            self.stack.append(OP_R)
                            self.current_state = A
                        else:
                            self.current_state = ERROR
                    case 'lpar':
                        if (self.stack and self.stack.pop()) == B:
                            self.stack.append(OP_R)
                            self.stack.append(LPAR)
                            self.stack.append(A)
                            self.current_state = A
                        else:
                            self.current_state = ERROR
                    # go to state C
                    case _:
                        self.current_state = ERROR
            case 'a':
                match input:
                    # stay in state A
                    case 'var':
                        if (self.stack and self.stack.pop()) != A:
                            self.current_state = ERROR
                    case 'int':
                        if (self.stack and self.stack.pop()) != A:
                            self.current_state = ERROR
                    case 'op_a':
                        self.stack.append(A)
                    case 'lpar':
                        if (self.stack and self.stack.pop()) == A:
                            self.stack.append(LPAR)
                            self.stack.append(A)
                        else:
                            self.current_state = ERROR
                    case 'op_r':
                        if (self.stack and self.stack.pop()) == OP_R:
                            self.stack.append(A)
                        else:
                            self.current_state = ERROR
                    case 'rpar':
                        if (self.stack and self.stack.pop()) != LPAR:
                            self.current_state = ERROR
                    # go to state B
                    case 'rbrac':
                        if (self.stack and self.stack.pop()) == LBRAC:
                            self.current_state = B
                        else:
                            self.current_state = ERROR
                    case 'and':
                        self.stack.append(B)
                        self.current_state = B
                    case 'or':
                        self.stack.append(B)
                        self.current_state = B
                    # go to state C
                    case 'sequencing':
                        self.stack.append(C)
                        self.current_state = C
                    case 'then':
                        if (self.stack and self.stack.pop()) == IF:
                            self.stack.append(THEN)
                            self.stack.append(C)
                            self.current_state = C
                        else:
                            self.current_state = ERROR
                    case 'else':
                        if (self.stack and self.stack.pop()) == THEN:
                            self.stack.append(ELSE)
                            self.stack.append(C)
                            self.current_state = C
                        else:
                            self.current_state = ERROR
                    case 'fi':
                        if (self.stack and self.stack.pop()) == ELSE:
                            self.current_state = C
                        else:
                            self.current_state = ERROR
                    case 'do':
                        if (self.stack and self.stack.pop()) == WHILE:
                            self.stack.append(DO)
                            self.stack.append(C)
                            self.current_state = C
                        else:
                            self.current_state = ERROR
                    case 'od':
                        if (self.stack and self.stack.pop()) == DO:
                            self.current_state = C
                    # go to DONE state
                    case -1:
                        if (self.stack and self.stack.pop()):
                            self.current_state = ERROR
                        else:
                            self.current_state = DONE
                    case _:
                        self.current_state = ERROR
            case 'Done':
                print("Success!")
            case 'Error':
                print("Error parsing program")

class Node:
    def __init__(self, data, value):
        self.data = data
        self.value = value
        self.next = None

def parseTokens(tokens):
    head = Node(tokens[0].type, tokens[0].value)
    prev = head
    for t in range(1, len(tokens)):
        prev.next = Node(tokens[t].type, tokens[t].value)
        prev = prev.next

    node = head
    pda = PDA(node)

    while (pda.current_state!=ERROR and pda.current_state!=DONE):
        pda.step()
        print("State:", pda.current_state.upper())
    if pda.current_state==ERROR:
        print("Error")
    elif pda.current_state==DONE:
        print("Success!")
    else:
        print("We should not be in this state:", pda.current_state)