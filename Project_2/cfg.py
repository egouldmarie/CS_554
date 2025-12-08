class CFG_Node:
    """
    A CFG node containing the AST node associated with its block of code,
    the type of CFG node it is ("entry", "exit", "condition", or "other"),
    its associated label, the content from the AST, and a list of
    successors and predecessors in the graph.

    """
    def __init__(self, label, ast=None, type=None, content=None):
        self.ast = ast
        self.type = type
        self.label = label
        self.content = content

        self.succ = []
        self.pred = []
    
    def get_all_predecessors(self):
        def get_preds(predecessor, visited):
            if predecessor not in visited: 
                visited.append(predecessor)
                for pred in predecessor.pred:
                    get_preds(pred, visited)
        
        predecessors = []
        for pred in self.pred:
            get_preds(pred, predecessors)

        return predecessors
    
    def get_all_successors(self):
        def get_succs(successor, visited):
            if successor not in visited: 
                visited.append(successor)
                for succ in successor.succ:
                    get_succs(succ, visited)
        
        successors = []
        for succ in self.succ:
            get_succs(succ, successors)

        return successors

class CFG:
    """
    A class that representing a CFG, generated from a decorated AST.

    Args:
        ast: decorated AST root node
    """
    def __init__(self, ast):
        # list of all nodes
        self.nodes = []
        # set up entry and exit nodes
        self.entry = CFG_Node(label="entry", ast=ast, type='entry', content='ENTRY')
        self.exit = CFG_Node(label="exit", type='exit', content='EXIT')

        # construct the rest of the CFG
        self.entry.succ.append(self.node_from_cfg(ast, self.exit))

        # sort list of all nodes by label
        self.nodes.sort(key=lambda node: int(node.label))

        # add the entry and exit nodes to the list of all nodes
        self.nodes.insert(0, self.entry)
        self.nodes.append(self.exit)

        # retroactively add nodes to their successor's predecessors
        for node in self.nodes:
            for succ in node.succ:
                succ.pred.append(node)
    
    def node_from_cfg(self, ast, next_node):
        """
            Generates CFG node from the decorated AST.

            Args:
                ast: the decorated AST node associated with this CFG node
                next_node: the successor of the CFG node currently being created
        """
        if ast.type == "seq":
            return self.node_from_cfg(ast.children[0], self.node_from_cfg(ast.children[1], next_node))
        elif ast.type in ["assign", "skip"]:
            node = CFG_Node(label=ast.l, ast=ast, type="other", content=self.cfg_content_from_ast(ast))
            self.nodes.append(node)
            node.succ.append(next_node)
            return node
        elif ast.type == "while":
            node = CFG_Node(label=ast.children[0].l, ast=ast.children[0], type="condition", content=self.cfg_content_from_ast(ast))
            self.nodes.append(node)
            node.succ.append(self.node_from_cfg(ast.children[1], node))
            node.succ.append(next_node)
            return node
        elif ast.type == "if":
            node = CFG_Node(label=ast.children[0].l, ast=ast.children[0], type="condition", content=self.cfg_content_from_ast(ast))
            self.nodes.append(node)
            node.succ.append(self.node_from_cfg(ast.children[1], next_node))
            node.succ.append(self.node_from_cfg(ast.children[2], next_node))
            return node

    def cfg_content_from_ast(self, ast):
        """
        Generate string representation of .while code from AST node

        Args:
            ast: AST node

        Returns: string
        """
        ops = ["=", "<", ">", "<=", ">=", "and", "add", "sub", "mult", "or", "assign"]
        if ast.type in ["int", "var", "true", "false", "skip"]:
            return f"{ast.value}"
        elif ast.type in ops:
            left = ""
            if ast.children[0].type in ops and ast.type != "assign":
                left = f"({self.cfg_content_from_ast(ast.children[0])})"
            else:
                left = f"{self.cfg_content_from_ast(ast.children[0])}"
            right = ""
            if ast.children[1].type in ops and ast.type != "assign":
                right = f"({self.cfg_content_from_ast(ast.children[1])})"
            else:
                right = f"{self.cfg_content_from_ast(ast.children[1])}"
            return f"{left} {ast.value} {right}"
        elif ast.type == "not":
            return f"NOT[{self.cfg_content_from_ast(ast.children[0])}]"
        elif ast.type in ["if", "while"]:
            return f"{ast.type} {self.cfg_content_from_ast(ast.children[0])}"

    def generate_cfg_dot(self, filename="cfg.dot"):
        """
        Generate a Graphviz DOT file for visualizing the Control Flow Graph.
        
        Args:
            filename: Output filename for the DOT file
        """
        dot_content = ["digraph CFG {"]
        dot_content.append("    rankdir=TB;")  # Top to bottom layout
        dot_content.append("    node [shape=box, style=rounded];")
        dot_content.append("")
        
        # Add all nodes
        for node in self.nodes:
            label_str = f"{node.label}\\n{node.content}"
            
            # Color code by node type
            if node.type == 'entry':
                color = "green"
            elif node.type == 'exit':
                color = "red"
            elif node.type == 'condition':
                color = "lightblue"
            else:
                color = "white"
            
            node_id = f"node_{node.label}"
            dot_content.append(f'    "{node_id}" [label="{label_str}", fillcolor={color}, style="rounded,filled"];')
        
        dot_content.append("")
        
        # Add all edges
        for node in self.nodes:
            node_id = f"node_{node.label}"
            for s in range(len(node.succ)):
                suc = node.succ[s]
                succ_id = f"node_{suc.label}"
                if len(node.succ) > 1:
                    dot_content.append(f'    "{node_id}" -> "{succ_id}"[color="{"green" if s==0 else "red"}"];')
                else:
                    dot_content.append(f'    "{node_id}" -> "{succ_id}";')
        
        dot_content.append("}")
        
        # Write to file
        with open(filename, "w") as f:
            f.write("\n".join(dot_content))
        
        print(f"CFG DOT file '{filename}' generated successfully!")
    
    def remove_node(self, node):
        """"""
        preds = node.pred
        succs = node.succ

        self.nodes.remove(node)

        trim = set()
        for succ in succs:
            succ.pred.remove(node)
            for pred in preds:
                pred.succ.remove(node)
                if pred != succ:
                    if pred not in succ.pred:
                        succ.pred.append(pred)
                        pred.succ.append(succ)
                    else:
                        # unnecessary if branch
                        trim.add(pred)
                else:
                    # eliminated the content of a while loop
                    trim.add(pred)
        
        for node in trim:
            self.remove_node(node)
    