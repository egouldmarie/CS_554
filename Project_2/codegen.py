"""
filename:     codegen.py
authors:      Jaime Gould, Qinghong Shao, Warren Craft
created:      2025-10-14
last updated: 2025-11-23
description:  Implements the RISC_V_CodeGenerator class to convert a
              Control Flow Graph (CFG) produced from a WHILE language
              program to RISC-V assembly code using s registers.
              Created for CS 554 (Compiler Construction) at UNM.
"""

class RISC_V_CodeGenerator:
    """
    RISC-V Code Generator
    Uses register allocation strategy and stack machine when necessary
    """
    
    def __init__(self, name="generated_function"):
        """
        Initialize RISC-V code generator
        """
        self.code = []
        self.name = name

        self.pointer = 0
        self.max_stack = 0

        self.var_map = {}       # Map variable names to s registers (s1, s2, s3, ...)
        self.variables = []     # List of all variables in order

    def gen(self, instruction):
        """
        Add instruction to code list
        """
        self.code.append(instruction)
    
    def generate(self, nodes, optimizer) -> str:
        """
        Main code generation function - generates code from CFG
        
        Args:
            nodes: list of control flow graph nodes
            
        Returns:
            String containing RISC-V assembly code
        """
        # Collect variables from Optimizer
        self._collect_variables_from_optimizer(optimizer)
        
        # Generate code from CFG nodes
        self._generate_from_cfg(nodes)
        
        # Generate function prologue (load variables into s registers)
        self._emit_function_prologue()

        # Generate function epilogue (save s registers back to memory)
        self._emit_function_epilogue()

        self.code = self.prologue + self.code + self.epilogue
        
        return "\n".join(self.code)
    
    def _collect_variables_from_optimizer(self, optimizer):
        """
        Collect all variables from interference graph in optimizer
        """
        self.variables = [var for var in optimizer.interference_graph.nodes]
        self.variables = sorted(self.variables)
        
        # Map variables to s registers (s1, s2, s3, ...)
        for i, var in enumerate(self.variables):
            if i <= 10:
                self.var_map[var] = f"s{i+1}"
            else:
                self.var_map[var] = f"{i*8}(a0)"
    
    def _emit_function_prologue(self):
        """
        Generate function prologue - load variables from memory into s registers
        """
        self.prologue = []
        self.prologue.append(f".globl {self.name}")
        self.prologue.append(".text")
        self.prologue.append(f"{self.name}:")
        self.prologue.append("    # Function prologue")
        # allocate stack
        self.prologue.append("    # Allocate stack")
        self.prologue.append(f"    addi sp, sp, -{8*self.max_stack}")
        self.prologue.append("    # Variable array pointer in a0")
        
        # Load each variable into its corresponding s register
        for i, var in enumerate(self.variables):
            if i<=10:
                offset = i * 8  # offset = index * 8 (first variable at offset 0)
                s_reg = self.var_map[var]
                self.prologue.append(f"    # {s_reg}<-{var}")
                self.prologue.append(f"    ld {s_reg}, {offset}(a0)")
        
        self.prologue.append("")
    
    def _emit_function_epilogue(self):
        """
        Generate function epilogue - save s registers back to memory
        """
        self.epilogue = []
        self.epilogue.append("")
        self.epilogue.append("    # Function epilogue")
        # deallocate stack
        self.epilogue.append("    # Deallocate stack")
        self.epilogue.append(f"    addi sp, sp, {8*self.max_stack}")

        # Save each variable from its s register back to memory
        for i, var in enumerate(self.variables):
            if i<=10:
                offset = i * 8  # offset = index * 8
                s_reg = self.var_map[var]
                self.epilogue.append(f"    # {var}<-{s_reg}")
                self.epilogue.append(f"    sd {s_reg}, {offset}(a0)")
        
        self.epilogue.append("    ret")
    
    def _push(self, register="t0"):
        self.gen(f"    sd {register}, {self.pointer*8}(sp)")
        self.pointer = self.pointer + 1
        if self.pointer > self.max_stack:
            self.max_stack = self.pointer
    
    def _pop(self, register="t0"):
        self.pointer = self.pointer - 1
        self.gen(f"    ld {register}, {self.pointer*8}(sp)")
    
    def _generate_from_cfg(self, nodes):
        """
        Generate code from CFG node - main CFG traversal function
        
        Args:
            nodes: CFGNodes to process
        """
        for n in range(len(nodes)):
            node = nodes[n]
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
                if var_reg[-1] == ")":
                    # spillage
                    self.gen(f"    sd {result_reg}, {var_reg}")
                else:
                    self.gen(f"    mv {var_reg}, {result_reg}")
        else:
            self._generate_expression(ast)

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
            var_reg = self.var_map[var_name]
            if var_reg[-1] == ")":
                # variable is in address space, not s-register
                self.gen(f"    ld {result_reg}, {var_reg}")
                return result_reg
            else:
                return var_reg
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
    