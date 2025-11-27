"""
filename:     codegen_ast_to_c.py
authors:      Warren Craft
author note:  based on earlier work authored with project partners
              Jaime Gould & Qinghong Shao
created:      2025-11-23
last updated: 2025-11-24
description:  Implements the ASTToCodeGenerator class to convert an
              abstract syntax tree (AST) (produced from the scanning
              and parsing of a WHILE language program) to C code.
              Code based on the RISC_V_CodeGenerator class previously
              developed with co-authors Jaime Gould & Qing Shao.
              Created for CS 554 (Compiler Construction) at UNM.
"""

from typing import List, Any
from datetime import date


class ASTToCCodeGenerator:
    """
    C Code Generator.
    An alternative CCodeGenerator to allow the omission of empty
    code such as while() loops with a do loop that is effectively
    empty or if() constructs with an effectively empty else block.
    """
    
    def __init__(self, source="source_file.while",
                 output_filename="generated_file.c"):
        """
        Initialize a C code generator, optionally supplying the name
        of the original WHILE source file and then planned output
        file name. The filenames supplied in the initialization are
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
        return "    " * self.indent_level
    
    def gen(self, instruction):
        """
        Add instruction to code list
        """
        self.code.append(instruction)

    def generate(self, ast) -> str:
        '''
        Primary code generation function, eventually generating
        the entire C code file translation of the WHILE program upon
        which the AST is based.
        '''
        
        # Establish alpha-ordered list of all variables
        self._collect_variables(ast)

        # Generate the initial part of the C code
        self._gen_c_file_start()

        # first indentation level within main()
        self.indent_level += 1

        # Generate the WHILE-equivalent code from the AST
        self._generate_statement(ast)

        # Generate the end of the C code
        self._gen_c_file_end()

        return "\n".join(self.code)
    
    def _collect_variables(self, ast):
        """
        Collect all variables from AST
        """
        def collect_from_node(node, branch=0):
            if branch > self.max_branch: self.max_branch = branch
            if node.type == "var":
                if node.value not in self.variables:
                    self.variables.append(node.value)
            elif node.type in ["seq", "assign", "while"]:
                collect_from_node(node.children[0])
                collect_from_node(node.children[1])
            elif node.type == "if":
                collect_from_node(node.children[0])
                collect_from_node(node.children[1])
                collect_from_node(node.children[2])
            elif node.type in ["add", "sub", "mult", "and", "or", "not"]:
                collect_from_node(node.children[0])
                if len(node.children) > 1:
                    collect_from_node(node.children[1], branch+1)
            elif node.type in ["=", "<", "<=", ">", ">="]:
                collect_from_node(node.children[0])
                collect_from_node(node.children[1], branch+1)
        
        # for stmt in ast:
        collect_from_node(ast)
        
        self.variables.sort()
    
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
                    f"    printf(\"{self.variables[i]} = %lld \\n\", "
                    f"(long long)var_values[{i}]);\n"
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
        self.gen(f"    int64_t var_values[{num_vars}];")
        self.gen(f"")
        self.gen(f"    // Store the user-supplied initial values.")
        self.gen(f"    for (int i = 0; i < {num_vars}; i++) " + "{")
        self.gen(f"        var_values[i] = atoll(argv[i + 1]);")
        self.gen(f"    }}")
        self.gen(f"")
        self.gen(f"    // Declare & initialize the variables.")
    
        # Generate commands to declare & init the variables
        for i in range(num_vars):
            self.gen("    int64_t " + self.variables[i] + f" = var_values[{i}];")
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
                    f"    printf(\"{self.variables[i]} = %lld \\n\", "
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
            # self._generate_assignment(node)
            # self.gen(self._construct_statement(node))
            self.code += self._construct_statement(node)
        elif node.type == "if":
            _if_construct = self._construct_statement(node)
            if _if_construct:
                self.code += _if_construct
            # self._generate_if_statement(node)
        elif node.type == "while":
            _while_construct = self._construct_statement(node)
            if self._construct_statement(node):
                self.code += _while_construct
            # self._generate_while_statement(node)
        elif node.type == "skip":
            self._generate_skip_statement(node)
    
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
        Generally: we choose to effectively skip such skip statements,
        without adding any lines to the code
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
    