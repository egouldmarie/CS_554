"""
filename:     cfg.py
authors:      Warren Craft
author note:  Based on earlier and on-going work authored with
              project partners Jaime Gould & Qinghong Shao, with
              Jaime accomplishing a recent serious revamping and
              simplification.
created:      2025-11-23
last updated: 2025-11-30
description:  Implements the CFG class and related class and utility
              functions to represent and construct control flow graphs
              (CFGs) and CFG nodes. This file varies slightly from
              our group project version file of the same name.
              Created for CS 554 (Compiler Construction) at UNM.
"""

class CFG:
    """
    A CFG node containing the AST node associated with its block of code,
    the type of CFG node it is ("entry", "exit", "condition", or "other"),
    its associated label, the content from the AST, and a list of
    successors and predecessors in the graph.
    The associated non-class function node_from_cfg() defined further
    below has been slightly modified from the group project version to
    allow a fuller version of a node's associated AST in the case of
    the WHILE-DO and IF-THEN-ELSE nodes, in part to allow the 
    complete instantiation of the WHILE program's CFG to C Code.
    """
    def __init__(self, label, ast=None, type=None, content=None):
        self.ast = ast
        self.type = type
        self.label = label
        self.content = content

        self.succ = []
        self.pred = []

    def __repr__(self):
        # Two options to facilitate printing and debugging.
        if self.succ == []:
            return f"{self.content}"
        # (1) save this option here for future;
        #     see further below for alternative
        # elif self.type == 'var':
        #     return f"{self.value}"
        # return f"({self.label}) {self.content} --> {self.succ}"
        # (2) This option allows more circumscribed output of
        #     individual nodes.
        succ_labels = []
        for succ in self.succ:
            succ_labels.append("(" + str(succ.label) + ") " + succ.content)
        succ_labels_str = " ,".join(succ_labels)
        return f"({self.label}) {self.content} --> [{succ_labels_str}]"

def ast_to_cfg(ast):
    """
    Generate control flow graph (CFG) from a decorated abstract
    syntax tree (AST).
    Arg:
        ast: decorated AST root node
    Returns:
        entry, all_nodes: the entry node of the CFG and a list of
                          all nodes ordered by unique node labels
    """
    # set up entry and exit nodes
    entry = CFG(label="entry", ast=ast, type='entry', content='ENTRY')
    exit = CFG(label="exit", type='exit', content='EXIT')

    # construct the rest of the CFG
    all_nodes = []
    entry.succ.append(node_from_cfg(ast, exit, all_nodes))

    # sort list of all nodes by label
    all_nodes.sort(key=lambda node: int(node.label))

    # add the entry and exit nodes to the list of all nodes
    all_nodes.insert(0, entry)
    all_nodes.append(exit)

    # retroactively add nodes to their successor's predecessors
    for node in all_nodes:
        for succ in node.succ:
            succ.pred.append(node)

    return entry, all_nodes

def node_from_cfg(ast, next_node, all_nodes):
    """
    Utility function used by ast_to_cfg(), generating a CFG node
    from the corresponding node in the decorated AST.
    Args:
        ast:       the decorated AST node associated with the desire
                   CFG node to construct
        next_node: the successor of the CFG node currently being 
                   created
        all_nodes: array of all CFG nodes to which to append
                   newly generated nodes
    """

    if ast.type == "seq":
        return node_from_cfg(ast.children[0],
                node_from_cfg(ast.children[1], next_node, all_nodes), all_nodes)
    elif ast.type in ["assign", "skip"]:
        node = CFG(label=ast.l, ast=ast, type="other",
                   content=cfg_content_from_ast(ast))
        all_nodes.append(node)
        node.succ.append(next_node)
        return node
    elif ast.type == "while":
        # modifed the node creation below to include more details from
        # the associate AST at the WHILE node location
        # node = CFG(label=ast.children[0].l, ast=ast.children[0],
        #            type="condition", content=cfg_content_from_ast(ast))
        node = CFG(label=ast.children[0].l, ast=ast, type="condition",
                   content=cfg_content_from_ast(ast.children[0]))
        all_nodes.append(node)
        node.succ.append(node_from_cfg(ast.children[1], node, all_nodes))
        node.succ.append(next_node)
        return node
    elif ast.type == "if":
        # modifed the node creation below to include more details from
        # the associate AST at the IF node location
        # node = CFG(label=ast.children[0].l, ast=ast.children[0],
        #            type="condition", content=cfg_content_from_ast(ast))
        node = CFG(label=ast.children[0].l, ast=ast, type="condition",
                   content=cfg_content_from_ast(ast.children[0]))
        all_nodes.append(node)
        node.succ.append(node_from_cfg(ast.children[1], next_node, all_nodes))
        node.succ.append(node_from_cfg(ast.children[2], next_node, all_nodes))
        return node

def cfg_content_from_ast(ast):
    """
    Generate string representation of .while code from AST node.
    Args:
        ast: AST node
    Returns: string
    """
    ops = ["=", "<", ">", "<=", ">=", "and",
           "add", "sub", "mult", "or", "assign"]
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
    Generate a Graphviz DOT file for visualizing the control flow graph
    (CFG), using color-coding for blocks and edges.
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
        dot_content.append(
                f'    "{node_id}" [label="{label_str}", '
                f'fillcolor={color}, style="rounded,filled"];')

    dot_content.append("")

    # Add all edges
    for node in nodes:
        node_id = f"node_{node.label}"
        for s in range(len(node.succ)):
            suc = node.succ[s]
            succ_id = f"node_{suc.label}"
            if len(node.succ) > 1:
                dot_content.append(
                        f'    "{node_id}" -> "{succ_id}"'
                        f'[color="{"green" if s==0 else "red"}"];')
            else:
                dot_content.append(f'    "{node_id}" -> "{succ_id}";')

    dot_content.append("}")

    # Write to file
    with open(filename, "w") as f:
        f.write("\n".join(dot_content))

    print(f"CFG DOT file '{filename}' generated successfully!")
    print(f"CFG contains {len(nodes)} nodes.")
