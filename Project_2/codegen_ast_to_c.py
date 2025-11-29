"""
filename:     codegen_ast_to_c.py
authors:      Warren Craft
author note:  based on earlier work authored with project partners
              Jaime Gould & Qinghong Shao
created:      2025-11-23
last updated: 2025-11-25
description:  Implements the ASTToCodeGenerator class to convert an
              abstract syntax tree (AST), produced from the scanning
              and parsing of a WHILE language program, to C code.
              This code is based on the RISC_V_CodeGenerator class
              previously developed with co-authors Jaime Gould &
              Qing Shao.
              Created for CS 554 (Compiler Construction) at UNM.
"""

from typing import List, Any
from datetime import date


class ASTToC_Generator:
    """
    AST-to-C code cenerator class, encapsulating methods for
    generating C code from the abstract syntax tree (AST) of
    a simple WHILE language program.
    Resulting C code omits 'empty' code such as a while-do
    loop with a do block that is effectively empty (e.g.
    consisting of only 'skip' statements), an if-then-else
    construct where both the then/else blocks are effectively
    empty, or the else portion of an if-then-else construct
    where the else block is effectively empty.
    """
    
    def __init__(self, source="source_file.while",
                 output_filename="generated_file.c"):
        """
        Initialize an AST-to-C code generator, optionally supplying the
        name of the original WHILE source file and the planned output
        .c file name. The filenames supplied in the initialization are
        NOT used to actually determine the input and output files,
        but are used instead to construct the output file's header
        comments. The compiler.py program actually takes as an argument
        the desired WHILE program source file and constructs a related
        output filename.
        """
        self.code = []
        self.indent_level = 0   # Determines indentation
        self.source = source    # Original WHILE source file
        self.output_filename = output_filename
        self.variables = []     # List of all variables

        self.l = 0

        self.max_branch = 0

        self.type_to_value_map = {
            "add" : "+",
            "sub" : "-",
            "mult": "*",
            "and" : "&&",
            "or"  : "||",
            "="   : "==",
            "<"   : "<",
            "<="  : "<=",
            ">"   : ">",
            ">="  : ">="
        }
    
    def indent(self):
        """
        Return a multiple of an indentation string (used in
        constructing C code strings with appropriate indentation,
        based on the generator's global indent_level attribute).
        """
        return "    " * self.indent_level
    
    def gen(self, instruction):
        """
        Add instruction to code list
        """
        self.code.append(instruction)

    def generate(self, ast) -> str:
        '''
        Primary code generation function, eventually generating
        the entire C code file translation of the WHILE program
        upon which the AST is based.
        '''
        
        # Establish alpha-ordered list of all variables
        # self._collect_variables(ast)
        self.variables = []
        self._collect_vars_from_ast_node(ast)
        self.variables.sort()

        # Generate the initial part of the C code
        self._gen_c_file_start()

        # first indentation level within main()
        self.indent_level += 1

        # Generate the WHILE-equivalent code from the AST
        self._generate_statement(ast)

        # Generate the end of the C code
        self._gen_c_file_end()

        return "\n".join(self.code)
    
    def _collect_vars_from_ast_node(self, node):
        """
        Recursively construct a list of all variables appearing
        in the abstract syntax tree (AST) upon which the CFG is based.
        """
        if node is None:
            return
        
        if node.type == "var" and node.value not in self.variables:
            self.variables.append(node.value)
        elif hasattr(node, 'children'):
            for child in node.children:
                self._collect_vars_from_ast_node(child)
        
    def _gen_c_file_start(self):
        '''
        Generate the standard initial content of the .c file, including
        #includes, the initial construction of main(), and code for
        reading in command line arguments and assigning values to
        variables.
        '''
        num_vars = len(self.variables)
        printVars = " ".join(self.variables)
        # pre-construct code for displaying variable values
        print_values = ""
        for i in range(num_vars):
            print_values += (
                    f"    printf(\"{self.variables[i]} = %d \\n\", "
                    f"var_values[{i}]);\n"
            )
        today = date.today()
        date_string = today.strftime("%Y-%m-%d")

        self.gen(f"/**")
        self.gen(f" * filename: {self.output_filename}")
        self.gen(f" * created:  {date_string}")
        self.gen(f" * descr:    C program produced from the AST of")
        self.gen(f" *           {self.source}.")
        self.gen(f"*/")
        self.gen(f"")
        self.gen(f"#include <stdio.h>")
        self.gen(f"#include <stdlib.h>")
        self.gen(f"")
        self.gen(f"int main(int argc, char *argv[]) {{")
        self.gen(f"")
        self.gen(f"    // Check if correct num of args provided")
        self.gen(f"    if (argc != {num_vars + 1} " + "){")
        self.gen(f'        printf("Executable requires {num_vars} integer arguments.\\n");')
        self.gen(f'        printf("Usage: <filename> {printVars}\\n");')
        self.gen(f'        return EXIT_FAILURE;')
        self.gen(f'    }}')
        self.gen(f"")
        self.gen(f"    // Establish array to store the {num_vars} int values")
        self.gen(f"    int var_values[{num_vars}];")
        self.gen(f"")
        self.gen(f"    // Store the user-supplied initial values.")
        self.gen(f"    for (int i = 0; i < {num_vars}; i++) " + "{")
        self.gen(f"        var_values[i] = atoi(argv[i + 1]);")
        self.gen(f"    }}")
        self.gen(f"")
        self.gen(f"    // Declare & initialize the variables.")
    
        # Generate commands to declare & init the variables
        for i in range(num_vars):
            self.gen("    int " + self.variables[i] + f" = var_values[{i}];")
        self.gen(f"")
        self.gen(f'    printf("Initial variable values are:\\n");')
        self.gen(f"")

        # Generate commands to print initialized variable values
        self.gen(f"    // Print initialized variable values to verify:")
        self.gen(f'    printf("\\n");')
        self.gen(print_values)
        
    def _gen_c_file_end(self):
        '''
        Generate the standard ending content of the .c file.
        '''
        num_vars = len(self.variables)
        print_values = ""
        for i in range(num_vars):
            print_values += (
                    f"    printf(\"{self.variables[i]} = %d \\n\", "
                    f"{self.variables[i]});\n"
            )
        self.gen(f"")
        self.gen(f"    // Print final array values:")
        self.gen(f'    printf("\\nFinal variable values are: \\n");')
        self.gen(f'    printf("\\n");')
        self.gen(print_values)
        self.gen(f'    printf("\\n");')
        self.gen(f"")
        self.gen(f"    return EXIT_SUCCESS;")
        self.gen(f"")
        self.gen(f"}}")
    
    def _generate_statement(self, node):
        """
        Generate statement code
        """
        if node.type == "seq":
            self._generate_statement(node.children[0]) # left node
            self._generate_statement(node.children[1]) # right node
        elif node.type == "assign":
            self.code += self._construct_statement(node)
        elif node.type == "if":
            _if_construct = self._construct_statement(node)
            if _if_construct:
                self.code += _if_construct
        elif node.type == "while":
            _while_construct = self._construct_statement(node)
            if self._construct_statement(node):
                self.code += _while_construct
        elif node.type == "skip":
            _skip_construct = self._construct_statement(node)
            if _skip_construct:
                self.code += _skip_construct
    
    def _construct_statement(self, node):
        '''
        Construct statement code without immediately adding it
        to the output code, returning the construction (in the
        form of a (possibly empty) list of statement strings) to
        the calling function. Such constructions are ultimately
        added to self.code list of lines of code by the
        generate_statement() function.
        '''
        if node.type == "seq":
            return (
                self._construct_statement(node.children[0])   # left node
              + self._construct_statement(node.children[1]) ) # right node
        elif node.type == "assign":
            return self._construct_assignment(node)
        elif node.type == "if":
            return self._construct_if_statement(node)
        elif node.type == "while":
            return self._construct_while_statement(node)
        elif node.type == "skip":
            return self._construct_skip_statement(node)

    def _construct_skip_statement(self, node):
        '''
        Generate C code for a skip statement.
        Generally, we choose to effectively skip such skip statements,
        without adding any lines to the code. But we maintain the
        infrastructure for possibly modifying this approach in the
        future.
        '''
        return []
        
    def _construct_assignment(self, node):
        """
        Construct assignment statement code, and pass back up to
        more general construction method
        """
        var_name = node.children[0].value
        expr = node.children[1]
        
        _rhs = self._construct_expression(expr)
        return [self.indent() + var_name + " = " + _rhs + ";"]
        
    def _construct_if_statement(self, node):
        """
        Generate if statement code, and pass resulting lines of
        code back up to more general construction method
        """
        condition = node.children[0]
        true_block = node.children[1]
        else_block = node.children[2]

        condition_str = self._construct_expression(condition)
        self.indent_level += 1 # for constructing true/else blocks
        true_construct = self._construct_statement(true_block)
        else_construct = self._construct_statement(else_block)
        self.indent_level -= 1 # adjust after leaving true/else blocks
        if  true_construct == [] and else_construct == []:
            return []
        # else we have an if-then-else with at least one non-empty
        # block, so construct the lines of code and return
        if_construct = (
                [self.indent() + "if (" + condition_str + ") {"]
                + true_construct
        )
        if else_construct:
            # we have a non-empty else block
            if_construct = (
                    if_construct
                    + [self.indent() + "} else {"]
                    + else_construct
                    + [self.indent() + "}"] )
        else:
            # we have an empty else block, so omit the else portion
            if_construct = (
                    if_construct + [self.indent() + "}"])

        return if_construct
    
    def _construct_while_statement(self, node):
        """
        Construct C code for a WHILE() loop, and pass back up to
        more general construction method. An empty while() loop is
        one that has an effectively empty do block, like a sequence
        of skips, or other operations that themselves evaluate to 
        being empty.
        """
        condition = node.children[0]
        body = node.children[1]

        condition_str = self._construct_expression(condition)
        # self.gen(self.indent() + "while (" + condition_str + ") {")
        self.indent_level += 1 # for constructing while() loop body
        body_construct = self._construct_statement(body)
        self.indent_level -= 1 # adjust after leaving while() loop body
        if not body_construct:
            return []
        # else we have a non-empty while() loop,
        # so construct the lines of code and return
        print(f"body_construct = {body_construct}")
        print(f"condition_str = {condition_str}")
        while_construct = (
            [self.indent() + "while (" + condition_str + ") {"]
            + body_construct
            + [self.indent() + "}"]
        )
        return while_construct

    def _construct_expression(self, node):
        """
        Generate C code for an expression in the AST.
        Result gets passed back up to the calling function rather
        than being directly added to the self.code list.
        """
        if node.type == "int":
            # Integer constant
            value = node.value
            return str(value)
        elif node.type == "var":
            # Variable
            var_name = node.value
            return var_name
        elif node.type in ["true", "false"]:
            # Boolean constant
            return node.type
        elif node.type in ["add", "sub", "mult", "=", "<", ">",
                           "<=", ">=", "and", "or"]:
            # Binary operator
            _lhs = self._construct_expression(node.children[0])
            _rhs = self._construct_expression(node.children[1])
            return (_lhs + " " + self.type_to_value_map[node.type] +
                    " " + _rhs)
        elif node.type == "not":
            # Logical NOT (Unary Operator)
            not_arg = self._construct_expression(node.children[0])
            return "!(" + not_arg + ")"


class CFGToC_Generator:
    """
    CFG-to-C code generator class, based on previously-developed
    RISC-V Code Generator, encapsulating methods for
    generating C code from the control flow graph (CFG) of a
    simple WHILE language program.
    Resulting C code omits 'empty' code such as a while-do
    loop with a do block that is effectively empty (e.g.
    consisting of only 'skip' statements), an if-then-else
    construct where both the then/else blocks are effectively
    empty, or the else portion of an if-then-else construct
    where the else block is effectively empty.
    
    """
    
    def __init__(self, source="source_file.while",
                 output_filename="generated_file.c"):
        """
        Initialize a CFG-to-C code generator, optionally supplying the
        name of the original WHILE source file and the planned output
        .c file name. The filenames supplied in the initialization are
        NOT used to actually determine the input and output files,
        but are used instead to construct the output file's header
        comments. The compiler.py program actually takes as an argument
        the desired WHILE program source file and constructs a related
        output filename.
        """
        self.code = []
        # self.name = name
        self.source = source    # Original WHILE source file
        self.output_filename = output_filename
        self.indent_level = 0

        self.pointer = 0
        self.max_stack = 0

        self.var_map = {}       # Map variable names to s registers (s1, s2, s3, ...)
        self.label_counter = 0
        self.variables = []     # List of all variables in order

        self.cfg = None          # The CFG being processed
        self.visited_nodes = set()  # Track visited CFG nodes
        self.label_to_asm_label = {}  # Map CFG label to assembly label
        print(f"\nCFGToC_Generator Initialized!\n")
        print(f"\nself.variables = {self.variables}")

    def indent(self): # DONE
        """
        Return a multiple of an indentation string (used in
        constructing C code strings with appropriate indentation,
        based on the generator's global indent_level attribute).
        """
        return "    " * self.indent_level

    def gen(self, instruction: str): # DONE
        """
        Add instruction string to code list.
        """
        self.code.append(instruction)
    
    def generate(self, cfg_nodes) -> str:
        '''
        Primary code generation function, eventually generating
        the entire C code file translation of the WHILE program
        upon which the CFG is based.
        '''

        # Prepare to track CFG nodes visited
        self.visited_nodes.clear()

        # Establish alpha-ordered list of all variables,
        # collecting variables from CFG nodes
        self._collect_variables_from_cfg(cfg_nodes)
        print(f"\nself.variables = {self.variables}\n")

        # Generate the initial part of the C code
        self._gen_c_file_start()

        # first indentation level within main()
        self.indent_level += 1

        # Generate the WHILE-equivalent code from the CFG
        # TBA
        # self._generate_statement(ast)

        # Generate the end of the C code
        self._gen_c_file_end()

        return "\n".join(self.code)
    
    # def generate(self, nodes) -> str:
    #     """
    #     Main code generation function - generates code from CFG
    #     Args:
    #         nodes: list of control flow graph nodes
    #     Returns:
    #         String containing C code
    #     """
    #     self.visited_nodes.clear()
    #     self.label_to_asm_label.clear()
        
    #     # Collect variables from CFG nodes
    #     self._collect_variables_from_cfg(nodes)
        
    #     # Generate code from CFG nodes
    #     self._generate_from_cfg(nodes)
        
    #     # Generate function prologue (load variables into s registers)
    #     self._emit_function_prologue()

    #     # Generate function epilogue (save s registers back to memory)
    #     self._emit_function_epilogue()

    #     self.code = self.prologue + self.code + self.epilogue
        
    #     return "\n".join(self.code)
    
    def _collect_variables_from_cfg(self, nodes):
        """
        Construct a list of all variables appearing in the CFG.
        This uses the rot node of the CG and then relies on the AST
        from which the CFG is generated.
        """
        self.variables = []
        self._collect_vars_from_ast_node(nodes[0].ast)
        self.variables.sort()
    
    def _collect_vars_from_ast_node(self, node):
        """
        Recursively construct a list of all variables appearing
        in the abstract syntax tree (AST) upon which the CFG is based.
        """
        if node is None:
            return
        if node.type == "var" and node.value not in self.variables:
            self.variables.append(node.value)
        elif hasattr(node, 'children'):
            for child in node.children:
                self._collect_vars_from_ast_node(child)
    
    def _gen_c_file_start(self):
        '''
        Generate the standard initial content of the .c file, including
        #includes, the initial construction of main(), and code for
        reading in command line arguments and assigning values to
        variables.
        '''
        num_vars = len(self.variables)
        printVars = " ".join(self.variables)
        # pre-construct code for displaying variable values
        print_values = ""
        for i in range(num_vars):
            print_values += (
                    f"    printf(\"{self.variables[i]} = %d \\n\", "
                    f"var_values[{i}]);\n"
            )
        today = date.today()
        date_string = today.strftime("%Y-%m-%d")

        self.gen(f"/**")
        self.gen(f" * filename: {self.output_filename}")
        self.gen(f" * created:  {date_string}")
        self.gen(f" * descr:    C program produced from the CFG of")
        self.gen(f" *           {self.source}.")
        self.gen(f"*/")
        self.gen(f"")
        self.gen(f"#include <stdio.h>")
        self.gen(f"#include <stdlib.h>")
        self.gen(f"")
        self.gen(f"int main(int argc, char *argv[]) {{")
        self.gen(f"")
        self.gen(f"    // Check if correct num of args provided")
        self.gen(f"    if (argc != {num_vars + 1} " + "){")
        self.gen(f'        printf("Executable requires {num_vars} integer arguments.\\n");')
        self.gen(f'        printf("Usage: <filename> {printVars}\\n");')
        self.gen(f'        return EXIT_FAILURE;')
        self.gen(f'    }}')
        self.gen(f"")
        self.gen(f"    // Establish array to store the {num_vars} int values")
        self.gen(f"    int var_values[{num_vars}];")
        self.gen(f"")
        self.gen(f"    // Store the user-supplied initial values.")
        self.gen(f"    for (int i = 0; i < {num_vars}; i++) " + "{")
        self.gen(f"        var_values[i] = atoi(argv[i + 1]);")
        self.gen(f"    }}")
        self.gen(f"")
        self.gen(f"    // Declare & initialize the variables.")
    
        # Generate commands to declare & init the variables
        for i in range(num_vars):
            self.gen("    int " + self.variables[i] + f" = var_values[{i}];")
        self.gen(f"")
        self.gen(f'    printf("Initial variable values are:\\n");')
        self.gen(f"")

        # Generate commands to print initialized variable values
        self.gen(f"    // Print initialized variable values to verify:")
        self.gen(f'    printf("\\n");')
        self.gen(print_values)
        
    def _gen_c_file_end(self):
        '''
        Generate the standard ending content of the .c file.
        '''
        num_vars = len(self.variables)
        print_values = ""
        for i in range(num_vars):
            print_values += (
                    f"    printf(\"{self.variables[i]} = %d \\n\", "
                    f"{self.variables[i]});\n"
            )
        self.gen(f"")
        self.gen(f"    // Print final array values:")
        self.gen(f'    printf("\\nFinal variable values are: \\n");')
        self.gen(f'    printf("\\n");')
        self.gen(print_values)
        self.gen(f'    printf("\\n");')
        self.gen(f"")
        self.gen(f"    return EXIT_SUCCESS;")
        self.gen(f"")
        self.gen(f"}}")
    
    def _gen_c_from_cfg(self, cfg):
        '''
        Generate C code from the CFG nodes.
        '''
        pass

    
    def _generate_from_cfg(self, cfg_nodes):
        """
        Generate code from CFG nodes - main CFG traversal function
        
        Args:
            nodes: CFGNodes to process
        """
        for n in range(len(cfg_nodes)):
            node = cfg_nodes[n]
            self.gen(f"label_{node.label}:")
            self.gen(f"    # {node.content}")
            if node.type in ["entry", "exit"]:
                pass
            else:
                self._generate_from_ast(node.ast)
                if node.type == "condition":
                    self.gen(f"    beqz t0, label_{node.succ[1].label}")
                if node.succ[0].label != nodes[n+1].label:
                    self.gen(f"    j label_{node.succ[0].label}")
    
    def _generate_from_ast(self, ast):
        if ast.type == "skip":
            self.gen(f"    # skip")
        elif ast.type == "assign":
            var_reg = self.var_map[ast.children[0].value]
            
            # result will be in t0
            result_reg = self._generate_expression(ast.children[1])
            
            # Move result to variable's s register
            if result_reg != var_reg:
                self.gen(f"    mv {var_reg}, {result_reg}")
        else:
            self._generate_expression(ast)
    
    def _construct_expression(self, node):
        """
        Generate C code for an expression in the CFG.
        Result gets passed back up to the calling function rather
        than being directly added to the self.code list.
        """
        if node.type == "int":
            # Integer constant
            value = node.value
            return str(value)
        elif node.type == "var":
            # Variable
            var_name = node.value
            return var_name
        elif node.type in ["true", "false"]:
            # Boolean constant
            return node.type
        elif node.type in ["add", "sub", "mult", "=", "<", ">",
                           "<=", ">=", "and", "or"]:
            # Binary operator
            _lhs = self._construct_expression(node.children[0])
            _rhs = self._construct_expression(node.children[1])
            return (_lhs + " " + self.type_to_value_map[node.type] +
                    " " + _rhs)
        elif node.type == "not":
            # Logical NOT (Unary Operator)
            not_arg = self._construct_expression(node.children[0])
            return "!(" + not_arg + ")"

    def _generate_expression(self, node, result_reg="t0"):
        """
        Generate expression code, return the register containing result
        
        Args:
            node: AST node representing the expression
            result_reg: Optional register to store result (defaults to t0)
            
        Returns:
            String name of register containing the result
        """

        if node.type == "int":
            # Integer constant
            value = node.value
            self.gen(f"    li {result_reg}, {value}")
            return result_reg
        elif node.type == "var":
            # Variable - get its s register
            var_name = node.value
            return self.var_map[var_name]
        elif node.type in ["true", "false"]:
            # Boolean constant
            if node.type == "true":
                self.gen(f"    li {result_reg}, 1")
                return result_reg
            else:
                return "x0"     # x0 always contains 0
        elif node.type in ["add", "sub", "mult", "=", "<", ">", "<=", ">=", "and", "or"]:
            # Binary operation
            # Evaluate left expression
            left_reg = self._generate_expression(node.children[0])

            # Evaluate right expression
            if left_reg == "t0" and node.children[1].type not in ["int", "var"]:
                # push into stack
                self._push(left_reg)
                # right_reg = t0
                right_reg = self._generate_expression(node.children[1])
                left_reg = "t1"
                self._pop(left_reg)
            else:
                # left_reg = t0, right_reg = t1
                right_reg = self._generate_expression(node.children[1], "t1")

            # Perform operation
            if node.type == "add":
                self.gen(f"    add {result_reg}, {left_reg}, {right_reg}")
            elif node.type == "sub":
                self.gen(f"    sub {result_reg}, {left_reg}, {right_reg}")
            elif node.type == "mult":
                self.gen(f"    mul {result_reg}, {left_reg}, {right_reg}")
            elif node.type == "=":
                self.gen(f"    sub {result_reg}, {left_reg}, {right_reg}")
                self.gen(f"    seqz {result_reg}, {result_reg}")
            elif node.type == "<":
                self.gen(f"    slt {result_reg}, {left_reg}, {right_reg}")
            elif node.type == "<=":
                self.gen(f"    slt {result_reg}, {right_reg}, {left_reg}")
                self.gen(f"    xori {result_reg}, {result_reg}, 1")
            elif node.type == ">":
                self.gen(f"    slt {result_reg}, {right_reg}, {left_reg}")
            elif node.type == ">=":
                self.gen(f"    slt {result_reg}, {left_reg}, {right_reg}")
                self.gen(f"    xori {result_reg}, {result_reg}, 1")
            elif node.type == "and":
                self.gen(f"    and {result_reg}, {left_reg}, {right_reg}")
            elif node.type == "or":
                self.gen(f"    or {result_reg}, {left_reg}, {right_reg}")
            
            return result_reg
        elif node.type == "not":
            # Logical NOT (Unary Operator)
            operand_reg = self._generate_expression(node.children[0])
            self.gen(f"    seqz {result_reg}, {operand_reg}")
            return result_reg
        else:
            # Unknown type
            raise ValueError("Unknown type")
    