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

        self.stack = []
        self.pointer = 0
        self.max_stack = 0

        self.var_map = {}       # Map variable names to s registers (s1, s2, s3, ...)
        self.variables = []     # List of all variables in order

        self.temp_in_use = {"t0":False, "t1":False}

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
            optimizer: Optimizer instance with liveness analysis results
            
        Returns:
            String containing RISC-V assembly code
        """
        # Store optimizer for later use
        self.optimizer = optimizer
        
        # Collect variables from Optimizer
        self._collect_variables_from_optimizer(optimizer)
        
        # Generate code from CFG nodes
        self._generate_from_cfg(nodes)
        
        # Generate function prologue (load entry-live variables into s registers)
        self._emit_function_prologue()
        
        # Generate function epilogue (save exit-live variables back to memory)
        self._emit_function_epilogue()
        
        self.code = self.prologue + self.code + self.epilogue
        
        return "\n".join(self.code)
    
    def _collect_variables_from_optimizer(self, optimizer):
        """
        Collect variables using Live Variable Analysis and Interference Graph coloring.
        Prioritizes entry-live variables and uses graph coloring for register allocation.
        """
        # Get entry-live variables (variables that are live at function entry)
        entry_live_vars = optimizer.IN.get("entry", set())
        
        # Get interference graph coloring
        coloring = optimizer.interference_graph.coloring
        
        # Get all variables from interference graph (all variables that appear in the program)
        all_vars = list(optimizer.interference_graph.nodes)
        
        # Calculate number of colors needed
        num_colors = len(set(coloring.values()))
        MAX_REGISTERS = 11  # s1-s11
        
        # Separate variables into entry-live and others
        entry_vars = [var for var in all_vars if var in entry_live_vars]
        other_vars = [var for var in all_vars if var not in entry_live_vars]
        
        # Sort for consistent ordering
        entry_vars = sorted(entry_vars)
        other_vars = sorted(other_vars)
        
        # Priority: entry-live variables first, then others
        # This ensures we allocate registers to the most important variables
        self.variables = entry_vars + other_vars
        
        # Map variables to registers using interference graph coloring
        # Variables with the same color can share a register (they don't interfere)
        color_to_register = {}  # Maps color -> register name
        register_count = 0
        
        # Assign registers based on coloring
        # Priority: colors used by entry-live variables get registers first
        entry_colors = set()
        for var in entry_vars:
            if var in coloring:
                entry_colors.add(coloring[var])
        
        # First pass: assign registers to colors (prioritizing entry-live variable colors)
        all_colors = set(coloring.values())
        # Sort colors: entry-live colors first, then others
        sorted_colors = sorted(entry_colors) + sorted(all_colors - entry_colors)
        
        for color in sorted_colors:
            if register_count < MAX_REGISTERS:
                # Assign to s register
                color_to_register[color] = f"s{register_count + 1}"
                register_count += 1
        
        # Second pass: map each variable to its register or memory location
        for var in self.variables:
            if var in coloring:
                color = coloring[var]
                if color in color_to_register:
                    # Variable gets a register (shared with other variables of same color)
                    self.var_map[var] = color_to_register[color]
                else:
                    # Variable is spilled to memory - use its position in variable array
                    var_index = self.variables.index(var)
                    self.var_map[var] = f"{var_index * 8}(a0)"
            else:
                # Variable not in coloring (shouldn't happen)
                raise ValueError("Variable not in graph coloring")
        
        # Store information about which variables are in registers vs memory
        self.vars_in_registers = [var for var in self.variables 
                                  if var in self.var_map and not self.var_map[var].endswith("(a0)")]
        self.vars_in_memory = [var for var in self.variables 
                              if var in self.var_map and self.var_map[var].endswith("(a0)")]
        
        # total number of s-registers used
        s_registers = set()
        for var in self.variables:
            if not self.var_map[var].endswith("(a0)"):
                s_registers.add(self.var_map[var])

        print(f"Register allocation: {len(self.vars_in_registers)} variables in {len(s_registers)} registers, "
              f"{len(self.vars_in_memory)} variables spilled to memory\n{self.var_map}")
        
        # Allow unused s registers to be used for stack
        for i in range(len(s_registers)+1, MAX_REGISTERS):
            self.stack.append(f"s{i}")
        print(f"Stack: {self.stack}")
    
    def _emit_function_prologue(self):
        """
        Generate function prologue - load entry-live variables from memory into s registers.
        Only loads variables that are allocated to registers (not spilled to memory).
        """
        self.prologue = []
        self.prologue.append(f".globl {self.name}")
        self.prologue.append(".text")
        self.prologue.append(f"{self.name}:")
        self.prologue.append("    # Function prologue")
        # allocate stack
        if self.max_stack > 0:
            self.prologue.append("    # Allocate stack")
            self.prologue.append(f"    addi sp, sp, -{8*self.max_stack}")
        else:
            self.prologue.append("    # Stack not needed")
        self.prologue.append("    # Variable array pointer in a0")
        
        # Load ONLY entry-live variables that are in registers (not spilled)
        # According to Task 9: only load variables that are live at entry
        entry_live_vars = self.optimizer.IN.get("entry", set())
        
        for var in self.variables:
            # Only load if: 1) variable is entry-live, 2) variable is in a register
            if var in entry_live_vars:
                var_reg = self.var_map.get(var)
                if var_reg and not var_reg.endswith("(a0)"):  # Variable is in a register
                    # Calculate offset based on variable's position in sorted list of all variables
                    var_index = self.variables.index(var)
                    offset = var_index * 8  # offset = index * 8 (first variable at offset 0)
                    self.prologue.append(f"    # {var_reg}<-{var} (entry-live)")
                    self.prologue.append(f"    ld {var_reg}, {offset}(a0)")
        
        self.prologue.append("")
    
    def _emit_function_epilogue(self):
        """
        Generate function epilogue - save variables that are live at exit back to memory.
        Only saves variables that are in registers (not already in memory).
        """
        self.epilogue = []
        self.epilogue.append("")
        self.epilogue.append("    # Function epilogue")
        # deallocate stack
        if self.max_stack > 0:
            self.epilogue.append("    # Deallocate stack")
            self.epilogue.append(f"    addi sp, sp, {8*self.max_stack}")

        # Save ONLY exit-live variables that are in registers back to memory
        # According to Task 9: only save variables that are live at exit (typically just "output")
        exit_live_vars = self.optimizer.OUT.get("exit", set())
        
        for var in self.variables:
            # Only save if: 1) variable is exit-live, 2) variable is in a register
            if var in exit_live_vars:
                var_reg = self.var_map.get(var)
                if var_reg and not var_reg.endswith("(a0)"):  # Variable is in a register
                    # Calculate offset based on variable's position
                    var_index = self.variables.index(var)
                    offset = var_index * 8  # offset = index * 8
                    self.epilogue.append(f"    # {var}<-{var_reg} (exit-live)")
                    self.epilogue.append(f"    sd {var_reg}, {offset}(a0)")
        
        self.epilogue.append("    ret")
    
    def _push(self, register="t0"):
        self.gen("    # push")
        if self.pointer >= len(self.stack):
            self.gen(f"    sd {register}, {(self.pointer-len(self.stack))*8}(sp)")
        else:
            self.gen(f"    mv {self.stack[self.pointer]}, {register}")
        self.pointer = self.pointer + 1
        if self.pointer - len(self.stack) > self.max_stack:
            # keep track of max stack size in order to allocate appropriate space
            self.max_stack = self.pointer - len(self.stack)
    
    def _pop(self, register="t0"):
        self.gen("    # pop")
        self.pointer = self.pointer - 1
        if self.pointer >= len(self.stack):
            self.gen(f"    ld {register}, {(self.pointer-len(self.stack))*8}(sp)")
        else:
            self.gen(f"    mv {register}, {self.stack[self.pointer]}")
    
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
            self.temp_in_use["t0"] = False
            self.temp_in_use["t1"] = False

            var_reg = self.var_map[ast.children[0].value]
            
            # result will be in t0
            result_reg = self._generate_expression(ast.children[1])
            
            # Move result to variable's s register or memory
            if result_reg != var_reg:
                if var_reg.endswith("(a0)"):
                    # Variable is spilled to memory
                    self.gen(f"    sd {result_reg}, {var_reg}")
                else:
                    # Variable is in a register
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
            if node.value == 0:
                return "x0"
            else:
                self.gen(f"    li {result_reg}, {value}")
                self.temp_in_use[result_reg] = True
                return result_reg
        elif node.type == "var":
            # Variable - get its register or memory location
            var_name = node.value
            var_reg = self.var_map.get(var_name)
            if var_reg and var_reg.endswith("(a0)"):
                # Variable is spilled to memory, load it into result register
                self.gen(f"    ld {result_reg}, {var_reg}")
                return result_reg
            elif var_reg:
                # Variable is in a register
                return var_reg
            else:
                # Variable not found (shouldn't happen, but handle gracefully)
                raise ValueError(f"Variable {var_name} not found in var_map")
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
            left_reg = self._generate_expression(node.children[0], result_reg)

            # Evaluate right expression
            need_to_pop = False
            right_reg = result_reg
            # determine which register to potentially store
            # result of evaluated right expression
            if left_reg == result_reg:
                right_reg = "t1" if left_reg == "t0" else "t0"
                if self.temp_in_use[right_reg]:
                    # if temporary register is already in use,
                    # store value in register in the stack
                    self._push(right_reg)
                    # mark for popping back after operation
                    need_to_pop = True

            right_reg = self._generate_expression(node.children[1], right_reg)

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

            if need_to_pop:
                # return previous value to the temporary register used
                # to hold the right side of the expression
                self._pop(right_reg)
                self.temp_in_use[right_reg] = True

            if result_reg in ["t0", "t1"]:
                self.temp_in_use[result_reg] = True

            return result_reg
        elif node.type == "not":
            # Logical NOT (Unary Operator)
            operand_reg = self._generate_expression(node.children[0])
            self.gen(f"    seqz {result_reg}, {operand_reg}")
            return result_reg
        else:
            # Unknown type
            raise ValueError("Unknown type")
    