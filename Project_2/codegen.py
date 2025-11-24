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
    Uses register allocation strategy instead of stack machine model
    """
    
    def __init__(self, name="generated_function"):
        """
        Initialize RISC-V code generator
        """
        self.code = []
        self.name = name
        self.var_map = {}       # Map variable names to s registers (s1, s2, s3, ...)
        self.label_counter = 0
        self.variables = []     # List of all variables in order
        self.cfg = None          # The CFG being processed
        self.visited_nodes = set()  # Track visited CFG nodes
        self.label_to_asm_label = {}  # Map CFG label to assembly label

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
    
    def gen(self, instruction):
        """
        Add instruction to code list
        """
        self.code.append(instruction)
    
    def generate(self, cfg) -> str:
        """
        Main code generation function - generates code from CFG
        
        Args:
            cfg: ControlFlowGraph object
            
        Returns:
            String containing RISC-V assembly code
        """
        self.cfg = cfg
        self.visited_nodes.clear()
        self.label_to_asm_label.clear()
        
        # Collect variables from CFG nodes
        self._collect_variables_from_cfg()
        
        # Generate function prologue (load variables into s registers)
        self._emit_function_prologue()
        
        # Generate code from CFG starting from entry node
        if cfg.entry_node:
            self._generate_from_cfg(cfg.entry_node)
        
        # Generate function epilogue (save s registers back to memory)
        self._emit_function_epilogue()
        
        return "\n".join(self.code)
    
    def _collect_variables_from_cfg(self):
        """
        Collect all variables from CFG nodes
        """
        variables_set = set()
        
        for node in self.cfg.nodes:
            if node.ast_node:
                self._collect_vars_from_ast_node(node.ast_node, variables_set)
        
        self.variables = sorted(list(variables_set))
        
        # Map variables to s registers (s1, s2, s3, ...)
        for i, var in enumerate(self.variables):
            self.var_map[var] = f"s{i+1}"
    
    def _collect_vars_from_ast_node(self, node, variables_set):
        """
        Recursively collect variables from an AST node
        """
        if node is None:
            return
        
        if node.type == "var":
            variables_set.add(node.value)
        elif hasattr(node, 'children'):
            for child in node.children:
                self._collect_vars_from_ast_node(child, variables_set)
    
    def _emit_function_prologue(self):
        """
        Generate function prologue - load variables from memory into s registers
        """
        self.gen(f".globl {self.name}")
        self.gen(".text")
        self.gen(f"{self.name}:")
        self.gen("    # Function prologue")
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
        Generate function epilogue - save s registers back to memory
        """
        self.gen("    # Function epilogue")
        
        # Save each variable from its s register back to memory
        for i, var in enumerate(self.variables):
            offset = i * 8  # offset = index * 8
            s_reg = self.var_map[var]
            self.gen(f"    # output<-{s_reg}")
            self.gen(f"    sd {s_reg}, {offset}(a0)")
        
        self.gen("    ret")
    
    def _generate_from_cfg(self, cfg_node):
        """
        Generate code from CFG node - main CFG traversal function
        
        Args:
            cfg_node: CFGNode to process
        """
        if cfg_node is None or cfg_node in self.visited_nodes:
            return
        
        # Mark node as visited
        self.visited_nodes.add(cfg_node)
        
        # Generate label for this node if it has a label
        if cfg_node.label is not None:
            asm_label = self._get_asm_label(cfg_node.label)
            self.gen(f"{asm_label}:")
            # Add comment with CFG label and content
            if cfg_node.content:
                self.gen(f"    # Label {cfg_node.label}: {cfg_node.content}")
            else:
                self.gen(f"    # Label {cfg_node.label}")
        
        # Generate code based on node type
        if cfg_node.node_type == 'entry':
            # Entry node - just continue to successors
            for successor in cfg_node.successors:
                if successor not in self.visited_nodes:
                    self._generate_from_cfg(successor)
        elif cfg_node.node_type == 'exit':
            # Exit node - should not have successors, but handle gracefully
            pass
        elif cfg_node.node_type == 'assign':
            self._generate_cfg_assignment(cfg_node)
        elif cfg_node.node_type == 'skip':
            self.gen("    # skip")
            # Continue to successors
            for successor in cfg_node.successors:
                if successor not in self.visited_nodes:
                    self._generate_from_cfg(successor)
        elif cfg_node.node_type == 'condition':
            self._generate_cfg_condition(cfg_node)
            # Condition handling manages its own successors
        elif cfg_node.node_type == 'merge':
            # Merge node - just continue to successors
            for successor in cfg_node.successors:
                if successor not in self.visited_nodes:
                    self._generate_from_cfg(successor)
        else:
            # Unknown node type
            self.gen(f"    # Unknown node type: {cfg_node.node_type}")
            # Continue to successors
            for successor in cfg_node.successors:
                if successor not in self.visited_nodes:
                    self._generate_from_cfg(successor)
    
    def _get_asm_label(self, cfg_label):
        """
        Get or create assembly label for a CFG label
        """
        if cfg_label not in self.label_to_asm_label:
            self.label_to_asm_label[cfg_label] = f"label_{cfg_label}"
        return self.label_to_asm_label[cfg_label]
    
    def _generate_cfg_assignment(self, cfg_node):
        """
        Generate assignment code from CFG node using s registers
        """
        if not cfg_node.ast_node:
            # No AST node, just continue to successors
            for successor in cfg_node.successors:
                if successor not in self.visited_nodes:
                    self._generate_from_cfg(successor)
            return
        
        ast_node = cfg_node.ast_node
        if ast_node.type != "assign" or len(ast_node.children) < 2:
            # Invalid assignment, continue to successors
            for successor in cfg_node.successors:
                if successor not in self.visited_nodes:
                    self._generate_from_cfg(successor)
            return
        
        var_name = ast_node.children[0].value
        expr = ast_node.children[1]
        
        # Get the s register for this variable
        if var_name not in self.var_map:
            # Variable not found, continue to successors
            for successor in cfg_node.successors:
                if successor not in self.visited_nodes:
                    self._generate_from_cfg(successor)
            return
        
        var_reg = self.var_map[var_name]
        
        # Generate expression code - result will be in a temporary s register
        # Use t0 as temporary, then move to var_reg
        result_reg = self._generate_expression_cfg(expr, "t0")
        
        # Move result to variable's s register
        if result_reg != var_reg:
            self.gen(f"    mv {var_reg}, {result_reg}")
        
        # Continue to successors
        # For while loops, check if any successor is a visited condition node (back edge)
        for successor in cfg_node.successors:
            if successor.node_type == 'condition' and successor in self.visited_nodes:
                # This is a while loop back edge - jump back to condition label
                if successor.label is not None:
                    cond_label = self._get_asm_label(successor.label)
                    self.gen(f"    j {cond_label}")
                    # Don't process this successor again - it's a back edge
                    return  # Exit early, don't process other successors
            if successor not in self.visited_nodes:
                self._generate_from_cfg(successor)

    def _generate_cfg_condition(self, cfg_node):
        """
        Generate condition code from CFG node (for if/while)
        """
        if not cfg_node.ast_node:
            # No AST node, handle successors
            for successor in cfg_node.successors:
                if successor not in self.visited_nodes:
                    self._generate_from_cfg(successor)
            return
        
        # cfg_node.ast_node is already the condition expression node
        # (not the if/while node, but the condition expression itself)
        condition_expr = cfg_node.ast_node
        
        if not condition_expr:
            # No condition, handle successors
            for successor in cfg_node.successors:
                if successor not in self.visited_nodes:
                    self._generate_from_cfg(successor)
            return
        
        # Generate condition expression - result in t0
        result_reg = self._generate_expression_cfg(condition_expr, "t0")
        
        if len(cfg_node.successors) >= 2:
            # Has true and false branches
            true_successor = cfg_node.successors[0]
            false_successor = cfg_node.successors[1]
            
            # Get labels for branches
            if false_successor.label is not None:
                false_label = self._get_asm_label(false_successor.label)
            else:
                false_label = self._new_label()
            
            # Check if this is a while loop (body loops back to condition)
            # We need to check if any node in the true branch (body) loops back to this condition
            is_while_loop = False
            visited_in_check = set()
            nodes_to_check = [true_successor]
            
            while nodes_to_check and not is_while_loop:
                current = nodes_to_check.pop(0)
                if current in visited_in_check:
                    continue
                visited_in_check.add(current)
                
                for succ in current.successors:
                    if succ == cfg_node:  # Found a back edge to condition
                        is_while_loop = True
                        break
                    if succ not in visited_in_check and succ.node_type != 'exit':
                        nodes_to_check.append(succ)
            
            # Conditional jump - if condition is false (0), jump to false branch
            self.gen(f"    beqz {result_reg}, {false_label}")
            
            # True branch
            if true_successor not in self.visited_nodes:
                self._generate_from_cfg(true_successor)
            
            # For if statements (not while loops), need to jump past false branch
            if not is_while_loop:
                # Find merge node or end of false branch
                end_label = None
                # Check if false_successor is a merge node
                if false_successor.node_type == 'merge':
                    # Merge node - check its successors for the actual end
                    for merge_succ in false_successor.successors:
                        if merge_succ.label is not None:
                            end_label = self._get_asm_label(merge_succ.label)
                            break
                    if end_label is None:
                        end_label = self._new_label()
                else:
                    # Check false branch's successors for merge
                    for succ in false_successor.successors:
                        if succ.node_type == 'merge':
                            if succ.label is not None:
                                end_label = self._get_asm_label(succ.label)
                            else:
                                end_label = self._new_label()
                            break
                        elif succ.label is not None:
                            end_label = self._get_asm_label(succ.label)
                            break
                
                if end_label and end_label != false_label:
                    self.gen(f"    j {end_label}")
            
            # False branch label and code
            if false_successor.label is None:
                self.gen(f"{false_label}:")
            elif false_successor not in self.visited_nodes:
                # Label will be generated when processing the node
                pass
            
            if false_successor not in self.visited_nodes:
                self._generate_from_cfg(false_successor)
            
        elif len(cfg_node.successors) == 1:
            # Only one successor (shouldn't happen for condition, but handle gracefully)
            successor = cfg_node.successors[0]
            if successor not in self.visited_nodes:
                self._generate_from_cfg(successor)
        # else: no successors (shouldn't happen, but handled by caller)
    
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
        
        #self.gen("")
        #self.gen(f"    # While Statement")
        self.gen(f"{loop_label}:")
        
        # Generate condition code
        #self.gen(f"    # Condition")
        #self.gen("    # [")
        #l = self.l
        #self.l = self.l+1
        self._generate_expression(condition)
        #self.gen(f"    # ]{l}")
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

    def _generate_expression_cfg(self, node, result_reg=None):
        """
        Generate expression code using s registers, return the register containing result
        
        Args:
            node: AST node representing the expression
            result_reg: Optional s register to store result (if None, allocates a temp)
            
        Returns:
            String name of s register containing the result
        """
        if result_reg is None:
            # Allocate a temporary s register
            # We'll use t0 for temporary calculations (it's not used for variables)
            result_reg = "t0"
        
        if node.type == "int":
            # Integer constant
            value = node.value
            self.gen(f"    li {result_reg}, {value}")
            return result_reg
        elif node.type == "var":
            # Variable - get its s register
            var_name = node.value
            if var_name in self.var_map:
                var_reg = self.var_map[var_name]
                # If result_reg is different, copy
                if result_reg != var_reg:
                    self.gen(f"    mv {result_reg}, {var_reg}")
                return result_reg
            else:
                # Variable not found, use 0
                self.gen(f"    li {result_reg}, 0")
                return result_reg
        elif node.type in ["true", "false"]:
            # Boolean constant
            if node.type == "true":
                self.gen(f"    li {result_reg}, 1")
            else:
                self.gen(f"    li {result_reg}, 0")
            return result_reg
        elif node.type in ["add", "sub", "mult", "=", "<", ">", "<=", ">=", "and", "or"]:
            # Binary operation
            # Evaluate left operand into result_reg
            left_reg = self._generate_expression_cfg(node.children[0], result_reg)
            
            # Evaluate right operand into a temporary register (t0 if available, or reuse)
            # We need a second register for the operation
            right_reg = "t0" if result_reg != "t0" else "t1"  # Use t1 as fallback if t0 is in use
            
            # If result_reg is t0, we need to use a different register for right operand
            if result_reg == "t0":
                right_reg = "t1"  # Use t1 temporarily
            
            right_reg = self._generate_expression_cfg(node.children[1], right_reg)
            
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
            operand_reg = self._generate_expression_cfg(node.children[0], result_reg)
            self.gen(f"    seqz {result_reg}, {operand_reg}")
            return result_reg
        else:
            # Unknown type, return 0
            self.gen(f"    li {result_reg}, 0")
            return result_reg
        
    def _new_label(self):
        """
        Generate new label
        """
        self.label_counter += 1
        return f"label_{self.label_counter}"
    