
class Generator:
    '''
    Initial attempt to define and establish methods for a generator
    of RISC-V assembly code from the parse tree or AST produced by
    the scanner and parser of WHILE language programs.
    To get this class started, some of the code is initially based
    on some related AI Overview of some generic google search results,
    then adapted to our specific WHILE language and parser
    implementations.
    '''

    def __init__(self):
        '''
        Initialize a generator of RISC-V code given a syntax tree ast
        produced from a WHILE language program.
        '''
        self.code = []
        self.var_map = {}  # map var names to reg or mem locs
        self.next_reg = 8  # to begin: use x8 (or t0) for vars
    
    def _get_register(self, var_name):
        if var_name not in self.var_map:
            if self.next_reg <= 31:
                reg_name = f"x{self.next_reg}"
                self.var_map[var_name] = reg_name
                self.next_reg += 1
            else:
                # For more complex scenarios, might spill to memory
                raise NotImplementedError("Running our of registers.")
            
        return self.var_map[var_name]
    
    def gen(self, instruction):
        # a convenience utility fxn to reduce code length elsewhere
        self.code.append(instruction)
    
    def generate_assignment(self, var, expression):
        # a very simple starter case
        target_reg = self._get_register(var)
        if isinstance(expression, int):
            # use 'addi' to 'load immediate' (pg 139)?
            self.gen(f"addi {target_reg}, x0, {expression}")
        elif isinstance(expression, str):
            # simple case of another variable
            source_reg = self._get_register(expression)
            # use a form of 'move value' (mv rd rs, pf 139)?
            self.gen(f"addi {target_reg}, {source_reg}, 0")
    
    def generate_addition(self, result_var, operand1_var, operand2_var):
        # not immediately clear how to interpret the instruction
        # set provided in the RISC-V manual
        result_reg = self._get_register(result_var)
        op1_reg    = self._get_register(operand1_var)
        op2_reg    = self._get_register(operand2_var)
        self.gen(f"add {result_reg}, {op1_reg}, {op2_reg}")

    def get_riscv_code(self):
        return "n".join(self.code)
