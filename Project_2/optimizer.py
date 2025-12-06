class Optimizer:
    def __init__(self, cfg):
        """
        Class for optimizing code from a CFG,
        utilizes Live Variable Analysis.

        Args:
            cfg: A Control Flow Graph object.
        """
        # Initialize LV_in set, and LV_out set
        self.IN = {}
        self.OUT = {}
        self.GEN = {}
        self.KILL = {}
        for node in cfg.nodes:
            self.IN[node.label] = set()
            self.OUT[node.label] = set()
            self.GEN[node.label] = self.gen(node)
            self.KILL[node.label] = self.kill(node)

        # Print Live Variable Analysis Equations
        print(f"LV_in(l)  = gen(l) ∪ (LV_out(l) / kill(l))")
        print(f"LV_out(l) = U LV_in(l') | l' ∈ l's successors\n")
        for node in cfg.nodes:
            gen = self.GEN[node.label] if len(self.GEN[node.label]) > 0 else "∅"
            kill = self.KILL[node.label] if len(self.KILL[node.label]) > 0 else "∅"
            print(f"label_{node.label}: {node.content}")
            print(f"LV_in({node.label})  = {gen} ∪ (LV_out({node.label}) / {kill})")
            if node.label == "exit":
                lv_out = f"LV_out({node.label}) = ∅"
            else:
                lv_out = f"LV_out({node.label}) ="
            for s in range(len(node.succ)):
                if s!=0: lv_out = lv_out + " ∪"
                lv_out = lv_out + f" LV_in({node.succ[s].label})"
            print(lv_out)
            print("")

        # Solve Live Variable Analysis of CFG
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
        
        # Print Live Variable In and Out sets for each node in the CFG
        print(f"Live variable analysis completed in {iteration} iteration(s).")
        print("Results:\n")
        for node in cfg.nodes:
            print(f"label_{node.label}: {node.content}")
            _in = self.IN[node.label] if len(self.IN[node.label]) > 0 else "∅"
            _out = self.OUT[node.label] if len(self.OUT[node.label]) > 0 else "∅"
            print(f"LV_in({node.label})  = {_in}")
            print(f"LV_out({node.label}) = {_out}")
            print("")

    def LVA_out(self, cfg_node):
        if cfg_node.label is not "exit":
            for succ in cfg_node.succ:
                self.OUT[cfg_node.label] = self.OUT[cfg_node.label].union(self.IN[succ.label])

    def LVA_in(self, cfg_node):
        self.IN[cfg_node.label] = self.GEN[cfg_node.label].union(self.OUT[cfg_node.label].difference(self.KILL[cfg_node.label]))

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
    