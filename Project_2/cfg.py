class CFG:
    def __init__(self, label, ast=None, type=None, content=None):
        self.ast = ast
        self.type = type
        self.label = label
        self.content = content

        self.succ = []
    
    def __repr__(self):
        # To facilitate printing and debugging.
        if self.succ == []:
            return f"{self.content}"
        # elif self.type == 'var':
        #     return f"{self.value}"
        # return f"({self.label}) {self.content} --> {self.succ}"
        succ_labels = []
        for succ in self.succ:
            succ_labels.append("(" + str(succ.label) + ") " + succ.content)
        succ_labes_str = " ,".join(succ_labels)
        return f"({self.label}) {self.content} --> [{succ_labes_str}]"

def ast_to_cfg(ast):
    entry = CFG(label="entry", ast=ast, type='entry', content='ENTRY')
    exit = CFG(label="exit", type='exit', content='EXIT')

    all_nodes = []
    entry.succ.append(node_from_cfg(ast, exit, all_nodes))
    all_nodes.sort(key=lambda node: int(node.label))
    all_nodes.insert(0, entry)
    all_nodes.append(exit)
    return entry, all_nodes

def node_from_cfg(ast, next_node, all_nodes):
    if ast.type == "seq":
        return node_from_cfg(ast.children[0], node_from_cfg(ast.children[1], next_node, all_nodes), all_nodes)
    elif ast.type in ["assign", "skip"]:
        node = CFG(label=ast.l, ast=ast, type="other", content=cfg_content_from_ast(ast))
        all_nodes.append(node)
        node.succ.append(next_node)
        return node
    elif ast.type == "while":
        node = CFG(label=ast.children[0].l, ast=ast.children[0], type="condition", content=cfg_content_from_ast(ast))
        all_nodes.append(node)
        node.succ.append(node_from_cfg(ast.children[1], node, all_nodes))
        node.succ.append(next_node)
        return node
    elif ast.type == "if":
        node = CFG(label=ast.children[0].l, ast=ast.children[0], type="condition", content=cfg_content_from_ast(ast))
        all_nodes.append(node)
        node.succ.append(node_from_cfg(ast.children[1], next_node, all_nodes))
        node.succ.append(node_from_cfg(ast.children[2], next_node, all_nodes))
        return node

def cfg_content_from_ast(ast):
    ops = ["=", "<", ">", "<=", ">=", "and", "add", "sub", "mult", "or", "assign"]
    if ast.type in ["int", "var", "true", "false", "skip"]:
        return f"{ast.value}"
    elif ast.type in ops:
        left = ""
        if ast.children[0].type in ops and ast.type is not "assign":
            left = f"({cfg_content_from_ast(ast.children[0])})"
        else:
            left = f"{cfg_content_from_ast(ast.children[0])}"
        right = ""
        if ast.children[1].type in ops and ast.type is not "assign":
            right = f"({cfg_content_from_ast(ast.children[1])})"
        else:
            right = f"{cfg_content_from_ast(ast.children[1])}"
        return f"{left} {ast.value} {right}"
    elif ast.type == "not":
        return f"NOT[{cfg_content_from_ast(ast.children[0])}]"
    elif ast.type in ["if", "while"]:
        return f"{ast.type} {cfg_content_from_ast(ast.children[0])}"

def generate_cfg_dot(nodes, filename="cfg.dot"):
    """
    Generate a Graphviz DOT file for visualizing the Control Flow Graph.
    
    Args:
        nodes: list of Control Flow Graph nodes
        filename: Output filename for the DOT file
    """
    dot_content = ["digraph CFG {"]
    dot_content.append("    rankdir=TB;")  # Top to bottom layout
    dot_content.append("    node [shape=box, style=rounded];")
    dot_content.append("")
    
    # Add all nodes
    for node in nodes:
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
    for node in nodes:
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
    print(f"CFG contains {len(nodes)} nodes.")