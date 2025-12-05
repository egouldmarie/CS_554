class Optimizer:
    def __init__(self, cfg):
        self.cfg = cfg

        for node in cfg.nodes:
            kill = []
            gen = []
            if node.type is not "exit":
                kill = self.kill(node)
                gen = self.gen(node)

            print(f"label_{node.label}: {node.content}")
            print(f"kill_{node.label}:  {kill}")
            print(f"gen_{node.label}:   {gen}")
            print("")

    def LVA(self, cfg_node):
        LVout = self.LVout(cfg_node)
        LVin = self.LVin(cfg_node, LVout)

    def LVin(self, cfg_node, LVout):
        return []
    
    def LVout(self, cfg_node):
        return []
    
    def kill(self, cfg_node):
        kill = []
        if cfg_node.ast.type == "assign":
            kill.append(cfg_node.ast.children[0].value)
        return kill

    def gen(self, cfg_node):
        gen = []
        ops = ["=", "<", ">", "<=", ">=", "and", "add", "sub", "mult", "or"]
        def get_gen_var(ast, gen):
            if ast.type == "assign":
                get_gen_var(ast.children[1], gen)
            elif ast.type == "not":
                get_gen_var(ast.children[0], gen)
            elif ast.type in ops:
                get_gen_var(ast.children[0], gen)
                get_gen_var(ast.children[1], gen)
            elif ast.type == "var":
                if ast.value not in gen: gen.append(ast.value)
        
        get_gen_var(cfg_node.ast, gen)
        return gen
    