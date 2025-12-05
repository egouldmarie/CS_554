class Optimizer:
    def __init__(self, cfg):
        self.cfg = cfg
        self.IN = {}
        self.OUT = {}
        self.changed = {}

        for node in cfg.nodes:
            self.IN[node.label] = set()
            self.OUT[node.label] = set()

        iteration = 0
        changed = True
        while changed:
            changed = False
            for n in range(len(cfg.nodes)-1, -1, -1):
                node = cfg.nodes[n]
                old_out = self.OUT[node.label]
                old_in = self.IN[node.label]
                self.LVA_out(node)
                self.LVA_in(node)
                if old_out != self.OUT[node.label] or old_in != self.IN[node.label]:
                    changed = True
            iteration = iteration + 1
        
        print(f"Live variable analysis completed in {iteration} iteration(s).\n")
        for node in cfg.nodes:
            print(f"label_{node.label}: {node.content}")
            print(f"LV_in:  {self.IN[node.label]}")
            print(f"LV_out: {self.OUT[node.label]}")
            print("")

    def LVA_out(self, cfg_node):
        if cfg_node.label is not "exit":
            for succ in cfg_node.succ:
                self.OUT[cfg_node.label] = self.OUT[cfg_node.label].union(self.IN[succ.label])

    def LVA_in(self, cfg_node):
        self.IN[cfg_node.label] = self.gen(cfg_node).union(self.OUT[cfg_node.label].difference(self.kill(cfg_node)))

    def kill(self, cfg_node):
        kill = set()
        if cfg_node.ast and cfg_node.ast.type == "assign":
            kill.add(cfg_node.ast.children[0].value)
        return kill

    def gen(self, cfg_node):
        gen = set()
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
                gen.add(ast.value)
        
        if cfg_node.ast:
            get_gen_var(cfg_node.ast, gen)
        return gen
    