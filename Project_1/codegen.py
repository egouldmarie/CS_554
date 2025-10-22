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
        self.gen(f".globl {self.name}")
        self.gen(".text")
        self.gen(f"{self.name}:")
        self.gen("    # Function prologue")
        #self.gen("    addi sp, sp, -16")
        #self.gen("    sd ra, 8(sp)")
        #self.gen("    sd fp, 0(sp)")
        #self.gen("    addi fp, sp, 16")
        self.gen("    # Variable array pointer in a0")
        self.gen("")
    
    def _emit_function_epilogue(self):
        """
        Generate function epilogue
        """
        self.gen("")
        self.gen("    # Function epilogue")
        #self.gen("    ld ra, 8(sp)")
        #self.gen("    ld fp, 0(sp)")
        #self.gen("    addi sp, sp, 16")
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
        self._generate_expression(expr)
        self.gen("")
        self.gen(f"    # {var_name} := ")
        self.gen(f"    ld t0, 0(sp)")                   # load value from stack into a temporary register (t0)
        self.gen(f"    addi sp, sp, 8")                 # move stack pointer up
        
        var_offset = self.variables.index(var_name) * 8
        self.gen(f"    sd t0, {var_offset}(a0)")        # copy value from temporary register (t0) into argument memory

        # Store result to variable
        #var_reg = self._get_register(var_name)
        #if var_reg.startswith("mem_"):
            # Variable stored in memory
            #var_offset = self.variables.index(var_name) * 8
            #self.gen(f"    sd {result_reg}, {var_offset}(a0)")
        #else:
            # Variable stored in register
            #self.gen(f"    mv {var_reg}, {result_reg}")
    
    def _generate_expression(self, expr):
        """
        Generate expression code, return result register
        """
        if expr[0] == "int":
            # Integer constant
            value = expr[1]
            self.gen(f"")
            self.gen(f"    # n = {value}")
            self.gen(f"    li t0, {value}")             # put value into a temporary register (t0)
            self.gen(f"    addi sp, sp, -8")            # move stack pointer down
            self.gen(f"    sd t0, 0(sp)")               # copy value from temp register into stack
        elif expr[0] == "var":
            # Variable
            var_name = expr[1]
            #var_reg = self._get_register(var_name)
            self.gen(f"")
            self.gen(f"    # var {var_name}")
            var_offset = self.variables.index(var_name) * 8
            self.gen(f"    ld t0, {var_offset}(a0)")    # load value into a temporary register (t0)
            self.gen(f"    addi sp, sp, -8")            # move stack pointer down
            self.gen(f"    sd t0, 0(sp)")               # copy value from temp register into stack

            #if var_reg.startswith("mem_"):
                # Load from memory
            #    var_offset = self.variables.index(var_name) * 8
            #    temp_reg = self._get_temp_register()
            #    self.gen(f"    ld {temp_reg}, {var_offset}(a0)")
            #    return temp_reg
            #else:
                # Get from register
            #    return var_reg
        elif expr[0] == "add":
            # Addition
            self._generate_expression(expr[1]) 
            self._generate_expression(expr[2])
            self.gen(f"")
            self.gen(f"    # Addition")
            # pop once --> get value from right expression, load into a temp register
            self.gen(f"    ld t1, 0(sp)")       # load value from stack into a temporary register (t1)
            self.gen(f"    addi sp, sp, 8")     # move stack pointer up
            # pop twice --> get value from left expression, load into a temp register
            self.gen(f"    ld t0, 0(sp)")       # load value from stack into a temporary register (t0)
            #self.gen(f"    addi sp, sp, 8")     # move stack pointer up

            self.gen(f"    add t0, t0, t1")     # perform addition operation, place result in t0
            # push the result from the addition onto the stack
            #self.gen(f"    addi sp, sp, -8")    # move stack pointer down
            self.gen(f"    sd t0, 0(sp)")       # copy value from temp register (t0) into stack
        elif expr[0] == "sub":
            # Subtraction
            self._generate_expression(expr[1])
            self._generate_expression(expr[2])

            self.gen(f"")
            self.gen(f"    # Subtraction")
            self.gen(f"    ld t1, 0(sp)")
            self.gen(f"    addi sp, sp, 8")
            self.gen(f"    ld t0, 0(sp)")

            self.gen(f"    sub t0, t0, t1")

            self.gen(f"    sd t0, 0(sp)")
        elif expr[0] == "mult":
            # Multiplication
            self._generate_expression(expr[1])
            self._generate_expression(expr[2])

            self.gen(f"")
            self.gen(f"    # Multiplication")
            self.gen(f"    ld t1, 0(sp)")
            self.gen(f"    addi sp, sp, 8")
            self.gen(f"    ld t0, 0(sp)")

            self.gen(f"    mul t0, t0, t1")

            self.gen(f"    sd t0, 0(sp)")
        elif expr[0] == "=":
            # Equality comparison
            self._generate_expression(expr[1])
            self._generate_expression(expr[2])
            
            self.gen(f"")
            self.gen(f"    # Equality")
            self.gen(f"    ld t1, 0(sp)")
            self.gen(f"    addi sp, sp, 8")
            self.gen(f"    ld t0, 0(sp)")
            
            self.gen(f"    sub t0, t0, t1")
            self.gen(f"    seqz t0, t0")

            self.gen(f"    sd t0, 0(sp)")
        elif expr[0] == "<":
            # Less than comparison
            self._generate_expression(expr[1])
            self._generate_expression(expr[2])

            self.gen(f"")
            self.gen(f"    # Less Than")
            self.gen(f"    ld t1, 0(sp)")
            self.gen(f"    addi sp, sp, 8")
            self.gen(f"    ld t0, 0(sp)")
            
            self.gen(f"    slt t0, t0, t1")
            self.gen(f"    sd t0, 0(sp)")
        elif expr[0] == "<=":
            # Less than or equal comparison
            self._generate_expression(expr[1])
            self._generate_expression(expr[2])

            self.gen(f"")
            self.gen(f"    # Less Than or Equal")
            self.gen(f"    ld t1, 0(sp)")
            self.gen(f"    addi sp, sp, 8")
            self.gen(f"    ld t0, 0(sp)")
            
            self.gen(f"    slt t0, t0, t1")
            self.gen(f"    xori t0, t0, 1")

            self.gen(f"    sd t0, 0(sp)")
        elif expr[0] == ">":
            # Greater than comparison
            self._generate_expression(expr[1])
            self._generate_expression(expr[2])
            
            self.gen(f"")
            self.gen(f"    # Greater Than")
            self.gen(f"    ld t1, 0(sp)")
            self.gen(f"    addi sp, sp, 8")
            self.gen(f"    ld t0, 0(sp)")

            self.gen(f"    slt t0, t1, t0")

            self.gen(f"    sd t0, 0(sp)")
        elif expr[0] == ">=":
            # Greater than or equal comparison
            self._generate_expression(expr[1])
            self._generate_expression(expr[2])
            
            self.gen(f"")
            self.gen(f"    # Greater Than or Equal")
            self.gen(f"    ld t1, 0(sp)")
            self.gen(f"    addi sp, sp, 8")
            self.gen(f"    ld t0, 0(sp)")

            self.gen(f"    slt t0, t0, t1")
            self.gen(f"    xori t0, t0, 1")

            self.gen(f"    sd t0, 0(sp)")
        elif expr[0] in ["true", "false"]:
            # Boolean constant
            self.gen(f"")
            self.gen(f"    # boolean constant = {expr[0]}")
            self.gen(f"    addi sp, sp, -8")    # move stack pointer down
            if expr[0] == "true":
                self.gen(f"    li t0, 1")       # put 1 into a temporary register (t0)
                self.gen(f"    sd t0, 0(sp)")   # copy value from temp register into stack
            else:
                self.gen(f"    sd x0, 0(sp)")   # copy 0 from x0 (always 0) into stack
        elif expr[0] == "and":
            # Logical AND
            self._generate_expression(expr[1])
            self._generate_expression(expr[2])

            self.gen(f"")
            self.gen(f"    # AND")
            self.gen(f"    ld t1, 0(sp)")
            self.gen(f"    addi sp, sp, 8")
            self.gen(f"    ld t0, 0(sp)")

            self.gen(f"    and t0, t0, t1")

            self.gen(f"    sd t0, 0(sp)")
        elif expr[0] == "or":
            # Logical OR
            self._generate_expression(expr[1])
            self._generate_expression(expr[2])

            self.gen(f"")
            self.gen(f"    # OR")
            self.gen(f"    ld t1, 0(sp)")
            self.gen(f"    addi sp, sp, 8")
            self.gen(f"    ld t0, 0(sp)")

            self.gen(f"    or t0, t0, t1")
            
            self.gen(f"    sd t0, 0(sp)")
        elif expr[0] == "not":
            # Logical NOT
            self._generate_expression(expr[1])
            self.gen(f"")
            self.gen(f"    # NOT")
            self.gen(f"    ld t0, 0(sp)")

            self.gen(f"    seqz t0, t0")
            self.gen(f"    sd t0, 0(sp)")
    
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
    
    def _generate_if_statement(self, stmt):
        """
        Generate if statement code
        """
        condition = stmt[1]
        true_block = stmt[2]
        else_block = stmt[3]
        
        # Generate condition code
        self.gen("")
        self.gen("    # If Statement")
        self._generate_expression(condition)
        self.gen(f"    ld t0, 0(sp)")       # load value from stack into a temporary register (t0)
        self.gen(f"    addi sp, sp, 8")     # move stack pointer up
        
        # Generate labels
        else_label = self._new_label()
        #end_label = self._new_label()
        end_label = "end_" + else_label
        
        # Conditional jump
        self.gen("")
        self.gen(f"    beqz t0, {else_label}")
        
        # true block
        for stmt in true_block:
            self._generate_statement(stmt)
        
        self.gen(f"    j {end_label}")
        self.gen("")
        self.gen(f"{else_label}:")
        
        # else block
        for stmt in else_block:
            self._generate_statement(stmt)
        
        self.gen("")
        self.gen(f"{end_label}:")
    
    def _generate_while_statement(self, stmt):
        """
        Generate while statement code
        """
        condition = stmt[1]
        body = stmt[2]
        
        # Generate labels
        loop_label = self._new_label()
        #end_label = self._new_label()
        end_label = "end_" + loop_label
        
        self.gen("")
        self.gen(f"    # While Statement")
        self.gen(f"{loop_label}:")
        
        # Generate condition code
        self._generate_expression(condition)
        self.gen(f"    ld t0, 0(sp)")       # load value from stack into a temporary register (t0)
        self.gen(f"    addi sp, sp, 8")     # move stack pointer up
        
        # Conditional jump
        self.gen("")
        self.gen(f"    beqz t0, {end_label}")
        
        # Loop body
        for stmt in body:
            self._generate_statement(stmt)
        
        self.gen(f"    j {loop_label}")
        self.gen("")
        self.gen(f"{end_label}:")
    
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
