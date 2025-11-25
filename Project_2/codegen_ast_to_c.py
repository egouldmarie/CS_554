"""
filename:     c_codegen.py
authors:      Warren Craft
author note:  based on earlier work authored with project partners
              Jaime Gould & Qinghong Shao
created:      2025-11-23
last updated: 2025-11-24
description:  Implements the C_CodeGenerator class to convert an
              abstract syntax tree (AST) (produced from the scanning
              and parsing of a WHILE language program) to C code.
              Code based on the RISC_V_CodeGenerator class previously
              developed with co-authors Jaime Gould & Qing Shao.
              Created for CS 554 (Compiler Construction) at UNM.
"""

from typing import List, Any
from datetime import date

class CCodeGenerator:
    """
    C Code Generator
    """
    
    def __init__(self, name="generated_file.c"):
        """
        Initialize a C code generator.
        """
        self.code = []
        self.indent_level = 0   # Determines indentation
        self.name = name
        self.var_map = {}       # Map variable names to registers or memory locations
        self.next_reg = 8       # Start using registers from x8 (t0-t6)
        self.label_counter = 0
        self.variables = []     # List of all variables
        self.memory_offset = 0  # Memory offset counter

        self.l = 0

        #self.max_branch = 1
        self.max_branch = 0

        self.comment_map = {
            "add": "    # Addition",
            "sub": "    # Subtraction",
            "mult": "    # Multiplication",
            "and": "    # AND",
            "or": "    # OR",
            "=": "    # Equality",
            "<": "    # Less Than",
            "<=": "    # Less Than or Equal",
            ">": "    # Greater Than",
            ">=": "    # Greater Than or Equal"
            }
        self.riscv_map = {
            "add": "    add t0, t0, t1",
            "sub": "    sub t0, t0, t1",
            "mult": "    mul t0, t0, t1",
            "and": "    and t0, t0, t1",
            "or": "    or t0, t0, t1",
            "=": "    sub t0, t0, t1\n    seqz t0, t0",
            "<": "    slt t0, t0, t1",
            "<=": "    slt t0, t1, t0\n    xori t0, t0, 1",
            ">": "    slt t0, t1, t0",
            ">=": "    slt t0, t0, t1\n    xori t0, t0, 1"
        }

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
            #if isinstance(node, tuple):
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
        
        #for stmt in ast:
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
        self.gen(f" * filename: {self.name}")
        self.gen(f" * created:  {date_string}")
        self.gen(f" * descr:    C program produced from the AST of")
        self.gen(f" *           {self.name}.")
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
            self._generate_assignment(node)
        elif node.type == "if":
            self._generate_if_statement(node)
        elif node.type == "while":
            self._generate_while_statement(node)
        elif node.type == "skip":
            self._generate_skip_statement(node)
    
    def _generate_skip_statement(self, node):
        '''
        Generate C code for a skip statement.
        Generally: we choose to effectively skip such skip statements,
        without adding any lines to the code
        '''
        pass
    
    def _generate_assignment(self, node):
        """
        Generate assignment statement code
        """
        var_name = node.children[0].value
        expr = node.children[1]
        
        _rhs = self._generate_expression(expr)
        self.gen(self.indent() + var_name + " = " + _rhs + ";")
    
    def _generate_if_statement(self, node):
        """
        Generate if statement code
        """
        condition = node.children[0]
        true_block = node.children[1]
        else_block = node.children[2]

        condition_str = self._generate_expression(condition)
        self.gen(self.indent() + "if (" + condition_str + ") {")

        # indent inside the if()
        self.indent_level += 1

        # put the true block (even if it's empty)
        self._generate_statement(true_block)
        # remove the indent
        self.indent_level -= 1

        # future work: deal with possibly empty (skip) content
        # in the ELSE block, but don't worry for now
        # close the if-then, set up the else:
        self.gen(self.indent() + "} else {")
        # now working the else block, so indent
        self.indent_level += 1
        self._generate_statement(else_block)
        self.indent_level -= 1
        self.gen(self.indent() + "}")

    def _generate_while_statement(self, node):
        """
        Generate C code for a WHILE() loop
        """
        condition = node.children[0]
        body = node.children[1]

        condition_str = self._generate_expression(condition)
        self.gen(self.indent() + "while (" + condition_str + ") {")

        # indent inside the while() loop
        self.indent_level += 1

        # put the body block (even if it's empty)
        self._generate_statement(body)
        # remove the indent
        self.indent_level -= 1

        # close the while() loop:
        self.gen(self.indent() + "}")

    def _generate_expression(self, node):
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
            _lhs = self._generate_expression(node.children[0])
            _rhs = self._generate_expression(node.children[1])
            return (_lhs + " " + self.type_to_value_map[node.type] +
                    " " + _rhs)
        elif node.type == "not":
            # Logical NOT (Unary Operator)
            not_arg = self._generate_expression(node.children[0])
            return "!(" + not_arg + ")"
    