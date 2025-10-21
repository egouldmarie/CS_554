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
        self.var_map = {}  # Map variable names to registers or memory locations
        self.next_reg = 8  # Start using registers from x8 (t0-t6)
        self.label_counter = 0
        self.variables = []  # List of all variables
        self.memory_offset = 0  # Memory offset counter
    
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
        for stmt in ast:
            self._generate_statement(stmt)
        
        # Generate function epilogue
        self._emit_function_epilogue()
        
        return "\n".join(self.code)
    
    def _collect_variables(self, ast: List[Any]):
        """
        Collect all variables from AST
        """
        def collect_from_node(node):
            if isinstance(node, tuple):
                if node[0] == "var":
                    if node[1] not in self.variables:
                        self.variables.append(node[1])
                elif node[0] == "assign":
                    collect_from_node(node[1])
                    collect_from_node(node[2])
                elif node[0] in ["if", "while"]:
                    collect_from_node(node[1])
                    for stmt in node[2]:
                        collect_from_node(stmt)
                elif node[0] in ["add", "sub", "mult", "and", "or", "not"]:
                    collect_from_node(node[1])
                    if len(node) > 2:
                        collect_from_node(node[2])
                elif node[0] in ["=", "<", "<=", ">", ">="]:
                    collect_from_node(node[1])
                    collect_from_node(node[2])
        
        for stmt in ast:
            collect_from_node(stmt)
        
        self.variables.sort()
    
    def _emit_function_prologue(self):
        """
        Generate function prologue
        """
        self.gen(".text")
        self.gen(f".globl {self.name}")
        self.gen(f"{self.name}:")
        self.gen("    # Function prologue")
        self.gen("    addi sp, sp, -16")
        self.gen("    sd ra, 8(sp)")
        self.gen("    sd fp, 0(sp)")
        self.gen("    addi fp, sp, 16")
        self.gen("    # Variable array pointer in a1")
        self.gen("")
    
    def _emit_function_epilogue(self):
        """
        Generate function epilogue
        """
        self.gen("    # Function epilogue")
        self.gen("    ld ra, 8(sp)")
        self.gen("    ld fp, 0(sp)")
        self.gen("    addi sp, sp, 16")
        self.gen("    ret")
        self.gen("")
    
    def _generate_statement(self, stmt):
        """
        Generate statement code
        """
        if stmt[0] == "assign":
            self._generate_assignment(stmt)
        elif stmt[0] == "if":
            self._generate_if_statement(stmt)
        elif stmt[0] == "while":
            self._generate_while_statement(stmt)
        elif stmt[0] == "skip":
            pass
    
    def _generate_assignment(self, stmt):
        """
        Generate assignment statement code
        """
        var_name = stmt[1][1]
        expr = stmt[2]
        
        # Generate expression code
        result_reg = self._generate_expression(expr)
        
        # Store result to variable
        var_reg = self._get_register(var_name)
        if var_reg.startswith("mem_"):
            # Variable stored in memory
            var_offset = self.variables.index(var_name) * 8
            self.gen(f"    sd {result_reg}, {var_offset}(a1)")
        else:
            # Variable stored in register
            self.gen(f"    mv {var_reg}, {result_reg}")
    
    def _generate_expression(self, expr):
        """
        Generate expression code, return result register
        """
        if expr[0] == "int":
            # Integer constant
            value = expr[1]
            temp_reg = self._get_temp_register()
            self.gen(f"    li {temp_reg}, {value}")
            return temp_reg
        elif expr[0] == "var":
            # Variable
            var_name = expr[1]
            var_reg = self._get_register(var_name)
            if var_reg.startswith("mem_"):
                # Load from memory
                var_offset = self.variables.index(var_name) * 8
                temp_reg = self._get_temp_register()
                self.gen(f"    ld {temp_reg}, {var_offset}(a1)")
                return temp_reg
            else:
                # Get from register
                return var_reg
        elif expr[0] == "add":
            # Addition
            left_reg = self._generate_expression(expr[1])
            right_reg = self._generate_expression(expr[2])
            result_reg = self._get_temp_register()
            self.gen(f"    add {result_reg}, {left_reg}, {right_reg}")
            return result_reg
        elif expr[0] == "sub":
            # Subtraction
            left_reg = self._generate_expression(expr[1])
            right_reg = self._generate_expression(expr[2])
            result_reg = self._get_temp_register()
            self.gen(f"    sub {result_reg}, {left_reg}, {right_reg}")
            return result_reg
        elif expr[0] == "mult":
            # Multiplication
            left_reg = self._generate_expression(expr[1])
            right_reg = self._generate_expression(expr[2])
            result_reg = self._get_temp_register()
            self.gen(f"    mul {result_reg}, {left_reg}, {right_reg}")
            return result_reg
        elif expr[0] == "=":
            # Equality comparison
            left_reg = self._generate_expression(expr[1])
            right_reg = self._generate_expression(expr[2])
            result_reg = self._get_temp_register()
            self.gen(f"    sub {result_reg}, {left_reg}, {right_reg}")
            self.gen(f"    seqz {result_reg}, {result_reg}")
            return result_reg
        elif expr[0] == "<":
            # Less than comparison
            left_reg = self._generate_expression(expr[1])
            right_reg = self._generate_expression(expr[2])
            result_reg = self._get_temp_register()
            self.gen(f"    slt {result_reg}, {left_reg}, {right_reg}")
            return result_reg
        elif expr[0] == "<=":
            # Less than or equal comparison
            left_reg = self._generate_expression(expr[1])
            right_reg = self._generate_expression(expr[2])
            result_reg = self._get_temp_register()
            self.gen(f"    slt {result_reg}, {right_reg}, {left_reg}")
            self.gen(f"    xori {result_reg}, {result_reg}, 1")
            return result_reg
        elif expr[0] == ">":
            # Greater than comparison
            left_reg = self._generate_expression(expr[1])
            right_reg = self._generate_expression(expr[2])
            result_reg = self._get_temp_register()
            self.gen(f"    slt {result_reg}, {right_reg}, {left_reg}")
            return result_reg
        elif expr[0] == ">=":
            # Greater than or equal comparison
            left_reg = self._generate_expression(expr[1])
            right_reg = self._generate_expression(expr[2])
            result_reg = self._get_temp_register()
            self.gen(f"    slt {result_reg}, {left_reg}, {right_reg}")
            self.gen(f"    xori {result_reg}, {result_reg}, 1")
            return result_reg
        elif expr[0] in ["true", "false"]:
            # Boolean constant
            value = 1 if expr[0] == "true" else 0
            temp_reg = self._get_temp_register()
            self.gen(f"    li {temp_reg}, {value}")
            return temp_reg
        elif expr[0] == "and":
            # Logical AND
            left_reg = self._generate_expression(expr[1])
            right_reg = self._generate_expression(expr[2])
            result_reg = self._get_temp_register()
            self.gen(f"    and {result_reg}, {left_reg}, {right_reg}")
            return result_reg
        elif expr[0] == "or":
            # Logical OR
            left_reg = self._generate_expression(expr[1])
            right_reg = self._generate_expression(expr[2])
            result_reg = self._get_temp_register()
            self.gen(f"    or {result_reg}, {left_reg}, {right_reg}")
            return result_reg
        elif expr[0] == "not":
            # Logical NOT
            operand_reg = self._generate_expression(expr[1])
            result_reg = self._get_temp_register()
            self.gen(f"    seqz {result_reg}, {operand_reg}")
            return result_reg
    
    def _get_temp_register(self):
        """
        Get temporary register
        """
        if self.next_reg <= 15:
            reg_name = f"x{self.next_reg}"
            self.next_reg += 1
            return reg_name
        else:
            # Use a0 as temporary register
            return "a0"
    
    def _generate_if_statement(self, stmt):
        """
        Generate if statement code
        """
        condition = stmt[1]
        true_block = stmt[2]
        else_block = stmt[3]
        
        # Generate condition code
        condition_reg = self._generate_expression(condition)
        
        # Generate labels
        else_label = self._new_label()
        end_label = self._new_label()
        
        # Conditional jump
        self.gen(f"    beqz {condition_reg}, {else_label}")
        self.gen("")
        
        # true block
        for stmt in true_block:
            self._generate_statement(stmt)
        
        self.gen(f"    j {end_label}")
        self.gen(f"{else_label}:")
        self.gen("")
        
        # else block
        for stmt in else_block:
            self._generate_statement(stmt)
        
        self.gen(f"{end_label}:")
        self.gen("")
    
    def _generate_while_statement(self, stmt):
        """
        Generate while statement code
        """
        condition = stmt[1]
        body = stmt[2]
        
        # Generate labels
        loop_label = self._new_label()
        end_label = self._new_label()
        
        self.gen(f"{loop_label}:")
        self.gen("")
        
        # Generate condition code
        condition_reg = self._generate_expression(condition)
        
        # Conditional jump
        self.gen(f"    beqz {condition_reg}, {end_label}")
        self.gen("")
        
        # Loop body
        for stmt in body:
            self._generate_statement(stmt)
        
        self.gen(f"    j {loop_label}")
        self.gen(f"{end_label}:")
        self.gen("")
    
    def _new_label(self):
        """
        Generate new label
        """
        self.label_counter += 1
        return f"label_{self.label_counter}"

# Test function
def test_improved_generator():
    """
    Test improved code generator
    """
    sample_ast = [
        ("assign", ("var", "x"), ("int", 5)),
        ("assign", ("var", "y"), ("add", ("var", "x"), ("int", 3))),
        ("while", (">", ("var", "x"), ("int", 0)), [
            ("assign", ("var", "x"), ("sub", ("var", "x"), ("int", 1)))
        ])
    ]
    
    generator = RISC_V_CodeGenerator()
    assembly = generator.generate(sample_ast)
    
    print("Improved RISC-V Assembly Code:")
    print("=" * 50)
    print(assembly)
    print("\nVariables:", generator.variables)
    print("Variable map:", generator.var_map)

if __name__ == "__main__":
    test_improved_generator()
