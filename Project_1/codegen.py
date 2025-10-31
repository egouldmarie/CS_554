"""
filename:     codegen.py
authors:      Jaime Gould, Qinghong Shao, Warren Craft
created:      2025-10-14
last updated: 2025-10-27
description:  Implements the RISC_V_CodeGenerator class to convert an
              abstract syntax tree (AST) produced from the scanning
              and parsing of a WHILE language program to risc_v
              assembly code.
              Created for CS 554 (Compiler Construction) at UNM.
"""

from typing import List, Any

class RISC_V_CodeGenerator:
    """
    RISC-V Code Generator
    Uses register allocation strategy instead of stack machine model
    """
    
    def __init__(self, name="generated_function"):
        """
        Initialize RISC-V code generator
        """
        self.code = []
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
    
    def _get_register(self, var_name):
        """
        Allocate register for variable
        """
        if var_name not in self.var_map:
            if self.next_reg <= 15:  # Use t0-t6 registers
                reg_name = f"x{self.next_reg}"
                self.var_map[var_name] = reg_name
                self.next_reg += 1
            else:
                # Use memory when registers are insufficient
                self.var_map[var_name] = f"mem_{var_name}"
                self.memory_offset += 8
        
        return self.var_map[var_name]
    
    def gen(self, instruction):
        """
        Add instruction to code list
        """
        self.code.append(instruction)
    
    def generate(self, ast: List[Any]) -> str:
        """
        Main code generation function
        """

        self._collect_variables(ast)
        
        # Generate function prologue
        self._emit_function_prologue()
        
        # Generate code
        self._generate_statement(ast)
        
        # Generate function epilogue
        self._emit_function_epilogue()
        
        return "\n".join(self.code)
    
    def _collect_variables(self, ast: List[Any]):
        """
        Collect all variables from AST
        """
        def collect_from_node(node, branch=0):
            if branch > self.max_branch: self.max_branch = branch
            if isinstance(node, tuple):
                if node[0] == "var":
                    if node[1] not in self.variables:
                        self.variables.append(node[1])
                elif node[0] in ["seq", "assign", "while"]:
                    collect_from_node(node[1])
                    collect_from_node(node[2])
                elif node[0] == "if":
                    collect_from_node(node[1])
                    collect_from_node(node[2])
                    collect_from_node(node[3])
                elif node[0] in ["add", "sub", "mult", "and", "or", "not"]:
                    collect_from_node(node[1])
                    if len(node) > 2:
                        collect_from_node(node[2], branch+1)
                elif node[0] in ["=", "<", "<=", ">", ">="]:
                    collect_from_node(node[1])
                    collect_from_node(node[2], branch+1)
        
        for stmt in ast:
            collect_from_node(stmt)
        
        self.variables.sort()
    
    def _emit_function_prologue(self):
        """
        Generate function prologue
        """
        self.gen(f".globl {self.name}")
        self.gen(".text")
        self.gen(f"{self.name}:")
        self.gen("    # Function prologue")
        self.gen(f"    addi sp, sp, -{8*self.max_branch}")
        #self.gen("    sd ra, 8(sp)")
        #self.gen("    sd fp, 0(sp)")
        #self.gen("    addi fp, sp, 16")
        self.gen("    # Variable array pointer in a0")
        self.gen("")
    
    def _emit_function_epilogue(self):
        """
        Generate function epilogue
        """
        #self.gen("")
        self.gen("    # Function epilogue")
        #self.gen("    ld ra, 8(sp)")
        #self.gen("    ld fp, 0(sp)")
        self.gen(f"    addi sp, sp, {8*self.max_branch}")
        self.gen("    ret")
        #self.gen("")
    
    def _generate_statement(self, stmt):
        """
        Generate statement code
        """
        if stmt[0] == "seq":
            self._generate_statement(stmt[1]) # left node
            self._generate_statement(stmt[2]) # right node
        elif stmt[0] == "assign":
            self._generate_assignment(stmt)
        elif stmt[0] == "if":
            self._generate_if_statement(stmt)
        elif stmt[0] == "while":
            self._generate_while_statement(stmt)
        elif stmt[0] == "skip":
            self.gen(f"    # [skip]{self.l}")
            self.l = self.l+1
            #pass
    
    def _generate_assignment(self, stmt):
        """
        Generate assignment statement code
        """
        var_name = stmt[1][1]
        expr = stmt[2]
        
        # Generate expression code
        self.gen("    # [")
        l = self.l
        self.l = self.l+1
        self._generate_expression(expr)
        #self.gen("")
        #self.gen(f"    # {var_name} := ")
        self.gen(f"    ld t0, 0(sp)")                   # load value from stack into a temporary register (t0)
        
        var_offset = self.variables.index(var_name) * 8
        self.gen(f"    sd t0, {var_offset}(a0)")        # copy value from temporary register (t0) into argument memory
        self.gen(f"    # ]{self.number_to_subscript(l)}")

    def _generate_if_statement(self, stmt):
        """
        Generate if statement code
        """
        condition = stmt[1]
        true_block = stmt[2]
        else_block = stmt[3]
        
        # Generate condition code
        #self.gen("")
        #self.gen("    # If Statement")
        self.gen("    # [")
        l = self.l
        self.l = self.l+1
        self._generate_expression(condition)
        self.gen(f"    # ]{self.number_to_subscript(l)}")
        self.gen(f"    ld t0, 0(sp)")       # load value from stack into a temporary register (t0)
        
        # Generate labels
        label = self._new_label()
        else_label = "else_" + label
        end_label = "end_" + label
        
        # Conditional jump
        #self.gen("")
        self.gen(f"    beqz t0, {else_label}")
        
        # true block
        self._generate_statement(true_block)
        
        self.gen(f"    j {end_label}")
        #self.gen("")
        self.gen(f"{else_label}:")
        
        # else block
        self._generate_statement(else_block)
        
        #self.gen("")
        self.gen(f"{end_label}:")
    
    def _generate_while_statement(self, stmt):
        """
        Generate while statement code
        """
        condition = stmt[1]
        body = stmt[2]
        
        # Generate labels
        label = self._new_label()
        loop_label = "while_" + label
        end_label = "end_" + label
        
        #self.gen("")
        #self.gen(f"    # While Statement")
        self.gen(f"{loop_label}:")
        
        # Generate condition code
        #self.gen(f"    # Condition")
        self.gen("    # [")
        l = self.l
        self.l = self.l+1
        self._generate_expression(condition)
        self.gen(f"    # ]{self.number_to_subscript(l)}")
        self.gen(f"    ld t0, 0(sp)")       # load value from stack into a temporary register (t0)
        
        # Conditional jump
        #self.gen("")
        self.gen(f"    beqz t0, {end_label}")
        
        # Do
        #self.gen(f"    # Do")
        self._generate_statement(body)

        #self.gen("")        
        self.gen(f"    j {loop_label}")
        #self.gen(f"    # Od")
        self.gen(f"{end_label}:")

    def _generate_expression(self, expr, branch=0):
        """
        Generate expression code, store result in stack
        """
        if expr[0] == "int":
            # Integer constant
            value = expr[1]
            #self.gen(f"    # literal = {value}")
            self.gen(f"    li t0, {value}")             # put value into a temporary register (t0)
            self.gen(f"    sd t0, {8*branch}(sp)")       # copy value from temp register into stack
        elif expr[0] == "var":
            # Variable
            var_name = expr[1]
            #self.gen(f"    # var {var_name}")
            var_offset = self.variables.index(var_name) * 8
            self.gen(f"    ld t0, {var_offset}(a0)")    # load value into a temporary register (t0)
            self.gen(f"    sd t0, {8*branch}(sp)")       # copy value from temp register into stack
        elif expr[0] in ["true", "false"]:
            # Boolean constant
            #self.gen(f"    # boolean constant = {expr[0]}")
            if expr[0] == "true":
                self.gen(f"    li t0, 1")               # put 1 into a temporary register (t0)
                self.gen(f"    sd t0, {8*branch}(sp)")   # copy value from temp register into stack
            else:
                self.gen(f"    sd x0, {8*branch}(sp)")   # copy 0 from x0 (always 0) into stack
        elif expr[0] in ["add", "sub", "mult", "=", "<", ">", "<=", ">=", "and", "or"]:
            self._generate_expression(expr[1], branch)
            self._generate_expression(expr[2], branch+1)
            #self.gen(self.comment_map[expr[0]])
            self.gen(f"    ld t1, {8*(branch+1)}(sp)")   # load value from stack into a temporary register (t1)
            self.gen(f"    ld t0, {8*branch}(sp)")       # load value from stack into a temporary register (t0)

            self.gen(self.riscv_map[expr[0]])           # perform operation, place result in t0
            self.gen(f"    sd t0, {8*branch}(sp)")       # copy value from temp register (t0) into stack
        elif expr[0] == "not":
            # Logical NOT (Unary Operator)
            self._generate_expression(expr[1], branch)
            #self.gen(f"    # NOT")
            self.gen(f"    ld t0, {8*branch}(sp)")

            self.gen(f"    seqz t0, t0")
            self.gen(f"    sd t0, {8*branch}(sp)")
    
    def _get_temp_register(self):
        """
        Get temporary register
        """
        if self.next_reg <= 15:
            reg_name = f"x{self.next_reg}"
            self.next_reg += 1
            return reg_name
        #else:
            # Use a0 as temporary register
        #    return "a0"
    
    def _new_label(self):
        """
        Generate new label
        """
        self.label_counter += 1
        return f"label_{self.label_counter}"
    
    def number_to_subscript(num):
        subscript = ['₀', '₁', '₂', '₃', '₄', '₅', '₆', '₇', '₈', '₉']
        return ''.join([subscript[int(d)] for d in str(num)])
