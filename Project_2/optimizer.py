class InterferenceGraph:
    def __init__(self):
        self.nodes = set()
        self.edges = {}
    
    def addNode(self, node):
        self.nodes.add(node)
        if self.edges.get(node) == None:
            self.edges[node] = set()

    def addEdge(self, node1, node2):
        if self.edges.get(node1) != None:
            self.edges[node1].add(node2)
        else:
            self.edges[node1] = {node2}
        if self.edges.get(node2) != None:
            self.edges[node2].add(node1)
        else:
            self.edges[node2] = {node1}
    
    def greedyColor(self):
        """
        Function for creating a coloring of the Interference Graph.
        Adapted from Greedy Color Algorithm referenced on
        Wikipedia: https://en.wikipedia.org/wiki/Greedy_coloring
        """
        def firstColor(colors):
            color = 0
            while color in colors:
                color += 1
            return color

        self.coloring = dict()
        for node in self.nodes:
            usedColors = {self.coloring[nbr]
                                 for nbr in self.edges[node]
                                 if nbr in self.coloring}
            self.coloring[node] = firstColor(usedColors)
        
        print(f"Coloring: {self.coloring}")

class Optimizer:
    def __init__(self, cfg, outVars={'output'}):
        """
        Class for optimizing code from a CFG,
        utilizes Live Variable Analysis.

        Args:
            cfg: A Control Flow Graph object.
            outVars: A set of variables assumed to be live on exit.
        """
        self.cfg = cfg

        # Initialize LV_in set, and LV_out set
        self.IN = {}
        self.OUT = {}
        self.GEN = {}
        self.KILL = {}
        for node in self.cfg.nodes:
            self.IN[node.label] = set()
            if node.label == "exit":
                self.OUT[node.label] = outVars
            else:
                self.OUT[node.label] = set()
            self.GEN[node.label] = self.gen(node)
            self.KILL[node.label] = self.kill(node)

        # Print Live Variable Analysis Equations
        print(f"LV_in(l)  = gen(l) ∪ (LV_out(l) / kill(l))")
        print(f"LV_out(l) = U LV_in(l') | l' ∈ l's successors\n")
        for node in self.cfg.nodes:
            gen = self.GEN[node.label] if len(self.GEN[node.label]) > 0 else "∅"
            kill = self.KILL[node.label] if len(self.KILL[node.label]) > 0 else "∅"
            print(f"label_{node.label}: {node.content}")
            print(f"LV_in({node.label})  = {gen} ∪ (LV_out({node.label}) / {kill})")
            if node.label == "exit":
                lv_out = f"LV_out({node.label}) = "+"{'output'}"
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
            for n in range(len(self.cfg.nodes)-1, -1, -1):
                node = self.cfg.nodes[n]
                old_out = self.OUT[node.label]
                old_in = self.IN[node.label]
                self.LVA_out(node)
                self.LVA_in(node)
                if old_out != self.OUT[node.label] or old_in != self.IN[node.label]:
                    changed = True
            iteration = iteration + 1
        
        # Print Live Variable In and Out sets for each node in the CFG
        print(f"Live variable analysis completed in {iteration} iteration(s).")

        # Eliminate dead code using Live Variable sets
        self.eliminate_dead_code()

        print("Results:\n")
        for node in self.cfg.nodes:
            print(f"label_{node.label}: {node.content}")
            _in = self.IN[node.label] if len(self.IN[node.label]) > 0 else "∅"
            _out = self.OUT[node.label] if len(self.OUT[node.label]) > 0 else "∅"
            print(f"LV_in({node.label})  = {_in}")
            print(f"LV_out({node.label}) = {_out}")
            print("")
        
        # Generate Interference Graph
        self.create_interference_graph()

    def LVA_out(self, cfg_node):
        if cfg_node.label != "exit":
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
    
    def eliminate_dead_code(self):
        """
        Function for eliminating dead code in the CFG
        after constructing the Live Variable sets.

        Adapted from pseudocode on pg 523 in Chapter 10
        of Engineering a Compiler - 3rd Edition
        """

        print(f"Number of nodes before: {len(self.cfg.nodes)}")
        # Dead assignments in the CFG
        dead = set()
        nodes = [node for node in self.cfg.nodes]
        for node in nodes:
            if node.type not in ["entry", "exit"]:
                if node.ast.type == "assign":
                    var = node.ast.children[0].value
                    if var not in self.OUT[node.label]:
                        dead.add(f"label_{node.label}: {node.content}")
                        self.cfg.remove_node(node)
                elif node.ast.type == "skip":
                    dead.add(f"label_{node.label}: {node.content}")
                    self.cfg.remove_node(node)
        print(f"Number of nodes after: {len(self.cfg.nodes)}")
        print(f"Dead Nodes: {dead}\n")
    
    def create_interference_graph(self):
        """
        Function for creating the interference graph
        to help with assigning registers.
        """
        # Create the interference graph for variables
        self.interference_graph = InterferenceGraph()
        self.interference_graph.addNode("output")
        for node in self.cfg.nodes:
            _in = self.IN[node.label]
            _out = self.OUT[node.label]
            for var1 in _in:
                self.interference_graph.addNode(var1)
                for var2 in _in:
                    if var1 != var2:
                        self.interference_graph.addEdge(var1, var2)
            
            for var1 in _out:
                self.interference_graph.addNode(var1)
                for var2 in _out:
                    if var1 != var2:
                        self.interference_graph.addEdge(var1, var2)
        
        print(f"Interference Graph nodes: {self.interference_graph.nodes}")
        print(f"Interference Graph edges: {self.interference_graph.edges}")

        self.interference_graph.greedyColor()
    