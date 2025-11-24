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

class RISC_V_CodeGenerator:
    """
    RISC-V Code Generator
    """
    
    def __init__(self, name="generated_function"):
        """
        Initialize RISC-V code generator
        """
        self.code = []
        self.name = name
        self.var_map = {}       # Map variable names to registers or memory locations
        self.label_counter = 0
        self.variables = []     # List of all variables

        self.max_branch = 0

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
    
    def gen(self, instruction):
        """
        Add instruction to code list
        """
        self.code.append(instruction)
    
    def generate(self, ast) -> str:
        """
        Main code generation function
        """

        self._collect_variables(ast)
        
        self._emit_function_prologue()  # Generate function prologue
        self._generate_statement(ast)   # Generate code
        self._emit_function_epilogue()  # Generate function epilogue
        
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
        
        collect_from_node(ast)
        
        self.variables.sort()
        # map variables to s registers
        for i, var in enumerate(self.variables):
            self.var_map[var] = f"s{i+1}"
    
    def _emit_function_prologue(self):
        """
        Generate function prologue
        """
        self.gen(f".globl {self.name}")
        self.gen(".text")
        self.gen(f"{self.name}:")
        self.gen("    # Function prologue")
        self.gen(f"    addi sp, sp, -{8*self.max_branch}")
        self.gen("    # Variable array pointer in a0")
        # Load each variable into its corresponding s register
        for i, var in enumerate(self.variables):
            offset = i * 8  # offset = index * 8 (first variable at offset 0)
            s_reg = self.var_map[var]
            self.gen(f"    # {s_reg}<-input")
            self.gen(f"    ld {s_reg}, {offset}(a0)")
        
        self.gen("")
    
    def _emit_function_epilogue(self):
        """
        Generate function epilogue
        """
        self.gen("")
        self.gen("    # Function epilogue")
        self.gen(f"    addi sp, sp, {8*self.max_branch}")
        # Save each variable from its s register back to memory
        for i, var in enumerate(self.variables):
            offset = i * 8  # offset = index * 8
            s_reg = self.var_map[var]
            self.gen(f"    # output<-{s_reg}")
            self.gen(f"    sd {s_reg}, {offset}(a0)")

        self.gen("    ret")
    
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
            self.gen(f"    # label = {node.l}")
            self.gen("    # skip")
    
    def _generate_assignment(self, node):
        """
        Generate assignment statement code
        """
        var_name = node.children[0].value
        expr = node.children[1]
        
        # Generate expression code
        self.gen(f"    # label = {node.l}")
        self._generate_expression(expr)
        self.gen(f"    ld {self.var_map[var_name]}, 0(sp)")     # load value from stack into assigned variable register
        self.gen("")

    def _generate_if_statement(self, node):
        """
        Generate if statement code
        """
        condition = node.children[0]
        true_block = node.children[1]
        else_block = node.children[2]

        # Generate condition code
        self.gen(f"    # label = {condition.l}")
        self._generate_expression(condition)
        self.gen(f"    ld t0, 0(sp)")       # load value from stack into a temporary register (t0)
        
        # Generate labels
        label = self._new_label()
        else_label = "else_" + label
        end_label = "end_" + label
        
        # Conditional jump
        self.gen(f"    beqz t0, {else_label}")
        self.gen("")
        
        # true block
        self._generate_statement(true_block)
        
        self.gen(f"    j {end_label}")
        self.gen(f"{else_label}:")
        
        # else block
        self._generate_statement(else_block)
        
        self.gen(f"{end_label}:")
    
    def _generate_while_statement(self, node):
        """
        Generate while statement code
        """
        condition = node.children[0]
        body = node.children[1]

        # Generate labels
        label = self._new_label()
        loop_label = "while_" + label
        end_label = "end_" + label
        
        self.gen(f"{loop_label}:")
        
        # Generate condition code
        self.gen(f"    # label = {condition.l}")
        self._generate_expression(condition)
        self.gen(f"    ld t0, 0(sp)")       # load value from stack into a temporary register (t0)
        
        # Conditional jump
        self.gen(f"    beqz t0, {end_label}")
        self.gen("")
        
        # Do
        self._generate_statement(body)

        self.gen(f"    j {loop_label}")
        self.gen(f"{end_label}:")

    def _generate_expression(self, node, branch=0):
        """
        Generate expression code, store result in stack
        """
        if node.type == "int":
            # Integer constant
            value = node.value
            self.gen(f"    li t0, {value}")                     # put value into a temporary register (t0)
            self.gen(f"    sd t0, {8*branch}(sp)")              # copy value from temp register into stack
        elif node.type == "var":
            # Variable
            var_name = node.value
            self.gen(f"    mv t0, {self.var_map[var_name]}")    # move value into a temporary register (t0)
            self.gen(f"    sd t0, {8*branch}(sp)")              # copy value from temp register into stack
        elif node.type in ["true", "false"]:
            # Boolean constant
            if node.type == "true":
                self.gen(f"    li t0, 1")                       # put 1 into a temporary register (t0)
                self.gen(f"    sd t0, {8*branch}(sp)")          # copy value from temp register into stack
            else:
                self.gen(f"    sd x0, {8*branch}(sp)")          # copy 0 from x0 (always 0) into stack
        elif node.type in ["add", "sub", "mult", "=", "<", ">", "<=", ">=", "and", "or"]:
            self._generate_expression(node.children[0], branch)
            self._generate_expression(node.children[1], branch+1)
            self.gen(f"    ld t1, {8*(branch+1)}(sp)")          # load value from stack into a temporary register (t1)
            self.gen(f"    ld t0, {8*branch}(sp)")              # load value from stack into a temporary register (t0)

            self.gen(self.riscv_map[node.type])                 # perform operation, place result in t0
            self.gen(f"    sd t0, {8*branch}(sp)")              # copy value from temp register (t0) into stack
        elif node.type == "not":
            # Logical NOT (Unary Operator)
            self._generate_expression(node.children[0], branch)
            self.gen(f"    ld t0, {8*branch}(sp)")

            self.gen(f"    seqz t0, t0")
            self.gen(f"    sd t0, {8*branch}(sp)")

    def _new_label(self):
        """
        Generate new label
        """
        self.label_counter += 1
        return f"label_{self.label_counter}"
    