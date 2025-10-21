
# ======================== #
#    Useful constants      #
# (in alphabetical order)  #
# ======================== #
ADD       = "add"
AND       = "and"
ARITHFACT = 'arith_factor'
ARITHTERM = 'arith_term'
ARITHEXPR = 'arith_expr'
ASSIGN    = "assign"
BOOLFACT  = 'bool_factor'
BOOLTERM  = 'bool_term'
BOOLEXPR  = 'bool_expr'
BRACS     = 'bracs'
DO        = "do"
ELSE      = "else"
EXPR      = 'expr'
FALSE     = "false"
FI        = "fi"
IF        = "if"
IGN       = "ignore"
INT       = "int"
LBRAC     = "lbrac"
LPAR      = "lpar"
MISM      = "mismatch"
MULT      = "mult"
NEWL      = "newline"
NOT       = "not"
OD        = "od"
OP_A      = "op_a"
OP_R      = "op_r"
OR        = "or"
PARENS    = 'parens'
PROG      = 'prog'
RBRAC     = "rbrac"
RPAR      = "rpar"
SEQ       = "seq"
SKIP      = "skip"
STMT      = 'stmt'
STMTLIST  = 'stmt_list'
SUB       = "sub"
THEN      = "then"
TRUE      = "true"
VAR       = "var"
WHILE     = "while"

class Parser:
    '''
    Define and establish methods for a parser of a sequence of tokens
    produced by a separate scanner or lexer. Parser(tokens) takes as
    input a sequence of Token objects, each consisting of a length-4
    NamedTuple of the form (type, value, line, column) and returns both
    a parse tree AND an abstract syntax tree, by consuming the tokens
    one by one and using recursive functions to match the tokens
    against grammar rules.
    '''

    def __init__(self, tokens):
        '''
        Initiate a parser using a command like:
        my_parser = Parser(tokens)
        '''
        self.stack = []
        self.tokens = tokens
        self.current_pos = 0
        self.current_token_index = 0
        self.current_token = self.tokens[0] if self.tokens else None
        # At the top level, the program parse tree (PT) and program
        # abstract syntax tree (AST) will each be a nested tuple of
        # statements, each statement being a collection of nested
        # tuples (essentially sub-trees). The AST is a simplified
        # (abstracted) version of the PT, generated in parallel with
        # the generation of the PT.
        self.program_pt  = ()
        self.program_ast = ()

    def _advance(self):
        '''
        A utility function to move the current token pointer by
        one token, updating the current_token_index and the
        current_token.
        '''
        self.current_token_index += 1
        if self.current_token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token_index]
        else:
            self.current_token = None

    def consume(self, expected_type):
        '''
        If the current token (as found in self.current_token) matches
        the expected_type, consume (and return) the token and advance
        to the next token by calling the _advance() helper fxn.
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
        context-checking and deciding how to process the current token.
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
        Top-level method to start the parsing process, assuming
        the Parser has been initialized with an appropriate list of
        tokens associated with a program consisting of a sequence
        of statements.
        '''
        
        # _stmts = self.statement_seq()
        pt_stmts, ast_stmts = self.statement_seq()
        self.program_pt = ('prog',) + (pt_stmts,)
        self.program_ast = ('prog',) + (ast_stmts,)

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
            
        return (self.program_pt, self.program_ast)
    
    def statement_seq(self):
        '''
        Parsing a block or sequence of statements or commands,
        and returning the sequence as a list.
        A sequence of statements consists of one or more statements,
        such as a sequence of statements making up an entire program
        or a sequence of statements appearing in the 'then' block
        of an if-then-else structure, etc. A sequence could be a single
        statement or multiple statements separated by the sequencing
        symbol ';' (i.e. a semicolon).
        Note that a sequence never ends with the sequencing symbol ';'
        (because the ';' signals that another statement should follow).
        Note also that a sequence is never literally empty; instead, 
        an effectively 'empty sequence' must consist of one or more
        'skip' statements (this is also how the general if-then-else
        structure is used to produce just the if-then component).
        '''
        statement_block = []
        pt_statement_block = []
        ast_statement_block = []

        # Check for empty program
        if not self.tokens:
            raise SyntaxError("Empty program is not allowed. Use 'skip' for an empty program.")

        # begin with the very first statement
        # Process the first statement in the sequence.
        pt_stmt, ast_stmt = self.statement()
        if pt_stmt:
            pt_statement_block.append(pt_stmt)
            if ast_stmt != (SKIP,):
                ast_statement_block.append(ast_stmt)
        else:
            _last_token = self.tokens[self.current_token_index]
            _value = _last_token.value
            _line = _last_token.line
            raise SyntaxError(
                    "Parser.statement() method encountered a problematic "
                    f"statement on line {_line}. Last token processed "
                    f"was '{_value}' on line {_line}.")
        
        # Process subsequent statement(s) if we see seq op ';' .
        while self.peek(SEQ):
            self.consume(SEQ)
            pt_stmt, ast_stmt = self.statement()
            if pt_stmt:
                pt_statement_block.append(pt_stmt)
                if ast_stmt != (SKIP,):
                    ast_statement_block.append(ast_stmt)
            else:
                _last_token = self.tokens[self.current_token_index]
                _value = _last_token.value
                _line = _last_token.line
                raise SyntaxError(
                    "Parser.statement() discovered a missing or "
                    f"problematic statement on line {_line}. "
                    "Last token processed "
                    f"was '{_value}' on line {_line}."
                )
        
        # If the supposed sequence actually consisted of just a single
        # statement, treat it as a statement instead of a sequence
        if len(pt_statement_block) == 1:
            # return just the instruction instead of a list
            pt_statement_block = pt_statement_block[0]
        if len(ast_statement_block) == 1:
            ast_statement_block = ast_statement_block[0]
        return (pt_statement_block, ast_statement_block)

    def statement(self):
        '''
        Pursue different parsing method(s) based on current statement.
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
            pt_result, ast_result = self.parse_assignment_stmt()
            pt_result = (STMT, pt_result)
            return (pt_result, ast_result)
        
        # skip (e.g., if x > 0 then x := x + 1 else skip)
        if self.peek(SKIP):
            pt_result, ast_result = self.parse_skip_stmt()
            pt_result = (STMT, pt_result)
            return (pt_result, ast_result)
        
        # if-then-else (if x < y then x := 0 else y := 0)
        if self.current_token.type == IF:
            pt_result, ast_result = self.parse_if_stmt()
            pt_result = (STMT, pt_result)
            return (pt_result, ast_result)
        
        # while-do (while x < 10 do x := x + 1)
        if self.peek(WHILE):
            pt_result, ast_result = self.parse_while_stmt()
            pt_result = (STMT, pt_result)
            return (pt_result, ast_result)

    def parse_assignment_stmt(self):
        '''
        Parsing assignment statements of the form x := expr .
        Method assumes caller has already verified that the statement
        to be parsed is indeed an assignment statement.
        '''
        pt_left, ast_left = self.expr()
        self.consume(ASSIGN)
        pt_right, ast_right = self.expr()
        pt_result = (ASSIGN, pt_left, pt_right)
        ast_result = (ASSIGN, ast_left, ast_right)
        return (pt_result, ast_result)
    
    def parse_skip_stmt(self):
        '''
        Parsing of 'skip' statements, which might appear (e.g.) in
        the else block of an IF statement like this:
            if x > 0 then
              x := x + 1
            else
              skip
            fi;
        A skip statement does nothing and can generally be ignored.
        This needs to be included in the parse tree (PT) but can be
        omitted from the abstract syntax tree (AST).
        '''
        self.consume(SKIP)   # discard 'skip' token

        # We let local caller fxns decide what to do
        # with a SKIP (parse tree will keep; AST will ignore).
        pt_result  = (SKIP,)
        ast_result = (SKIP,)
        return (pt_result, ast_result)
    
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

        self.consume(IF)                   # discard 'if'
        # recursively parse boolean condition
        pt_condition, ast_condition = self.bool_expr() 
        self.consume(THEN)                 # discard 'then'
        
        # recursively parse the true block stmts
        pt_true_block, ast_true_block = self.statement_seq()
        
        self.consume(ELSE)                 # discard 'else'
        
        # recursively parse the else block stmts
        pt_else_block, ast_else_block = self.statement_seq()
            
        self.consume(FI)                   # discard 'fi'

        # Note that the true_block and/or else_block cannot generally
        # be literally empty but might consist of SKIP command(s), and
        # a SKIP might produce an empty block for the AST. We are
        # implicitly assuming the THEN block will NOT be empty.
        pt_result = (IF, pt_condition, THEN, pt_true_block,
                     ELSE, pt_else_block, FI)
        if isinstance(ast_else_block, list) and len(ast_else_block)==0:
            ast_result = (IF, ast_condition, ast_true_block)
        else:
            ast_result = (IF, ast_condition, ast_true_block, ast_else_block)
        return (pt_result, ast_result)

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
        # Recursively parse boolean condition
        pt_condition, ast_condition = self.bool_expr()
        self.consume(DO)               # discard 'do'
        
        # Recursively parse and return the while block of stmts
        pt_while_block, ast_while_block = self.statement_seq()
                                     
        self.consume(OD)               # discard 'od'

        # Can the while_block can be empty?
        pt_result  = (WHILE, pt_condition, DO, pt_while_block, OD)
        ast_result = (WHILE, ast_condition, ast_while_block)
        return (pt_result, ast_result)
    
    def expr(self):
        '''
        Handles either an arithmetic expression (e.g. x + 2 * y)
        or a boolean expression (e.g. x >= y).
        '''
        # distinguish boolean vs arithmetic expressions
        if (self.current_token.type in [LBRAC, NOT, AND, OR]):
            pt_result, ast_result = self.bool_expr()
        else:
            pt_result, ast_result = self.arith_expr()
        return (pt_result, ast_result)
    
    # ====================================== #
    # arithmetic expressions and components  #
    # SEE: arith_expr, term, factor          #
    # ====================================== #
    
    def arith_expr(self):
        '''
        For a sum or difference expression such as x + 2 * y (which
        then consists of arithmetic terms and factors).
        '''
        pt_result, ast_result = self.term()
        while (self.current_token
               and (self.current_token.value in ['+', '-'])):
            op_token = self.current_token
            if op_token.value == '+':
                self.consume(OP_A)
                pt_right, ast_right = self.term()
                pt_result = (ARITHEXPR, (ADD, pt_result, pt_right))
                ast_result = (ADD, ast_result, ast_right)
            else:
                # subtraction expression
                self.consume(OP_A)
                pt_right, ast_right = self.term()
                pt_result = (ARITHEXPR, (SUB, pt_result, pt_right))
                ast_result = (SUB, ast_result, ast_right)

        return (pt_result, ast_result)
    
    def term(self):
        '''
        For a participant (term) in a sum or difference expression.
        For example, in the expression 'x + 2 * y,'
        the 'x' and the '2 * y' are both terms.
        '''
        pt_result, ast_result = self.factor()
        while (self.current_token and self.current_token.value == '*'):
            op_token = self.consume(OP_A)
            pt_right, ast_right = self.factor()
            pt_result = (ARITHTERM, (MULT, pt_result, pt_right))
            ast_result = (MULT, ast_result, ast_right)
        return (pt_result, ast_result)
    
    def factor(self):
        '''
        For a participant in a multiplication, such a participant being
        a number, a variable, or a parenthesized expression.
        '''
        if self.peek(INT):
            token = self.consume(INT)
            pt_result = ('arith_factor', (INT, int(token.value)))
            ast_result = int(token.value)
            return (pt_result, ast_result)
        elif self.peek(VAR):
            token = self.consume(VAR)
            pt_result = ('arith_factor', (VAR, token.value))
            ast_result = token.value
            return (pt_result, ast_result)
        elif self.peek(LPAR):
            self.consume(LPAR)    # consume and discard '('
            # recursively parse and return inner expr
            pt_result, ast_result = self.expr()
            self.consume(RPAR)    # consume and discard ')'
            pt_result = ('arith_factor', (PARENS, pt_result))
            return (pt_result, ast_result)
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
        pt_result, ast_result = self.bool_term()
        if (self.current_token
               and (self.current_token.value == OR)):
            self.consume(OR)
            pt_right, ast_right = self.bool_term()
            pt_result = (BOOLEXPR, (OR, pt_result, pt_right))
            ast_result = (OR, ast_result, ast_right)
        return (pt_result, ast_result)
    
    def bool_term(self):
        '''
        For a boolean AND, whose components then might themselves be
        bool_expr, bool_term, or bool_factor.
        '''
        pt_result, ast_result = self.bool_factor()
        while (self.current_token and self.peek(AND)):
            self.consume(AND)
            pt_right, ast_right = self.bool_factor()
            pt_result  = (BOOLTERM, (AND, pt_result, pt_right))
            ast_result = (AND, ast_result, ast_right)
        return (pt_result, ast_result)
    
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
            # recursively parse and return inner expr
            pt_result, ast_result = self.bool_expr()
            self.consume(RBRAC)        # discard ]
            pt_result  = (BOOLFACT, (NOT, (BRACS, pt_result)))
            ast_result = (NOT, ast_result)
            return (pt_result, ast_result)
        elif self.peek(LBRAC):
            self.consume(LBRAC)        # discard [
            # recursively parse and return inner expr
            pt_result, ast_result = self.bool_expr()
            self.consume(RBRAC)        # discard ]
            pt_result = (BOOLFACT, (BRACS, pt_result))
            return (pt_result, ast_result)
        elif self.peek(TRUE):
            self.consume(TRUE)
            pt_result = (BOOLFACT, TRUE)
            ast_result = TRUE
            return (pt_result, ast_result)
        elif self.peek(FALSE):
            self.consume(FALSE)
            pt_result = (BOOLFACT, FALSE)
            ast_result = FALSE
            return (pt_result, ast_result)
        else:
            # we must have a relational expression such as x < y
            pt_left, ast_left = self.arith_expr()
            op = self.consume(OP_R).value
            pt_right, ast_right = self.arith_expr()

            pt_result = (BOOLFACT, (op, pt_left, pt_right))
            ast_result = (op, ast_left, ast_right)
            return (pt_result, ast_result)
    
    def ast_from_parse_tree(self, nested_tuple):
        '''
        Recursively produce a nested_tuple version of an abstract
        syntax tree (AST) from the generated nested-tuple version of
        the parse tree (PT). The AST is basically just a simplified
        version of the PT.
        This approach was chosen over trying to construct the PT and
        AST in parallel, in part because it simplifies the code and
        makes tweaks and modifications to the resulting AST easier.
        The comments use 'node' language, but we're dealing just with
        nested tuples instead of literal trees and tree nodes.
        '''

        # Interpret first element of a tuple as node's type.
        # A node's _value_ may be more complicated.
        node_type = nested_tuple[0]

        # the remaining elements (if any) are the children,
        # which themselves might be nested tuples
        children = nested_tuple[1:]

        # A dictionary to facilitate the choice of a 'value' for each
        # node, which in turn will be used eventually as the label for
        # the node in DOT language and visualization process. Most of
        # the time it makes sense to let the AST use the same labels
        # as found in the PT, but maybe abbreviate labels later (in
        # the transformation to a Tree with TreeNodes) when visualizing
        # the trees.
        type_to_value = {
            ADD:ADD, ASSIGN:ASSIGN, IF:IF, MULT:MULT, NOT:NOT,
            PROG:PROG, SEQ:SEQ, SUB:SUB, WHILE:WHILE,
            '<':'<', '>':'>', '<=':'<=', '>=':'>=', '=':'='
        }

        # here somewhere, if we have 'do', 'then', 'else' as node_type,
        # we just want to return the "sequence" or perhaps single item
        # that occurs in 2nd position.
        # Perhaps simply returning nested_tuple[1]? Or … the transformed
        # version of nested_tuple[1]
        # if we hit (do, [...], od)
        # if node_type in ['do', 'then', 'else']:
        #     _seq_block = []
        #     for instr in nested_tuple[1]:
        #         _seq_block.append(self.ast_from_parse_tree(instr))
        #     return _seq_block
        # TESTING to avoid block just above
        if node_type in ['do', 'then', 'else']:
            node_type = 'seq'
            children = (nested_tuple[1], )
        # END TESTING

        # Establish the current TreeNode
        # current_node = TreeNode(type=node_type, value=type_to_value[node_type])
        current_node = (type_to_value[node_type],)

        # Then recursively convert and add children, with some
        # specialization for various types.
        for child in children:
            if isinstance(child, tuple):
                # if child is a var or int type, treat it like a leaf
                if child[0] in ['var', 'int']:
                    current_node += (child[1], )
                else:
                    # if a child is some other nested tuple
                    child_node = self.ast_from_parse_tree(child)
                    if child_node:
                        current_node += (child_node, )
            
            elif isinstance(child, list):
                # a list corresponds to sequence of stmts inside a while
                # block, an if-true block, or if-else block.
                _type = 'seq'
                _value = type_to_value[_type]
                _seq_block = []
                for instr in child:
                    _seq_block.append(self.ast_from_parse_tree(instr))
                current_node += (_seq_block,)

            elif child in ['(', ')', '[', ']', 'fi', 'od']:
                # being explicit about this for clarity: simply
                # not including redundant details in the AST
                continue

            else:
                # child is a 'leaf' value, not a tuple
                _type = child_tuple
                print(f"_type = {_type}")
                _value = type_to_value[_type]
                print(f"_value = {_value}")
                current_node.children.append(TreeNode(type=_type, value=_value))

        return current_node


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
