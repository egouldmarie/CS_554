"""
filename:     cfg.py
authors:      Auto-generated for Project 2
created:      2025-11-18
last updated: 2025-11-21
description:  Implements Control Flow Graph (CFG) data structures and
              conversion from decorated AST to CFG.
              Created for CS 554 (Compiler Construction) at UNM.
"""

from trees import ADD, ASSIGN, IF, INT, MULT, SKIP, SEQ, SUB, VAR, WHILE


class CFGNode:
    """
    Represents a node in the Control Flow Graph.
    Each node corresponds to a labeled statement or condition in the program.
    """
    
    def __init__(self, label, node_type, content=None, ast_node=None):
        """
        Initialize a CFG node.
        
        Args:
            label: The label number (e.g., 0, 1, 2, ...)
            node_type: Type of node ('assign', 'skip', 'condition', 'entry', 'exit', 'merge')
            content: String description of the node content (optional)
            ast_node: Reference to the original AST node (optional)
        """
        self.label = label
        self.node_type = node_type  # 'assign', 'skip', 'condition', 'entry', 'exit', 'merge'
        self.content = content      # Human-readable description
        self.ast_node = ast_node    # Reference to AST node for code generation
        self.successors = []        # List of successor CFGNode objects
        self.predecessors = []       # List of predecessor CFGNode objects
    
    def add_successor(self, successor):
        """Add a successor node and update its predecessors."""
        if successor not in self.successors:
            self.successors.append(successor)
        if self not in successor.predecessors:
            successor.predecessors.append(self)
    
    def __repr__(self):
        content_str = f": {self.content}" if self.content else ""
        return f"CFGNode(label={self.label}, type={self.node_type}{content_str})"


class ControlFlowGraph:
    """
    Represents a Control Flow Graph for a WHILE program.
    """
    
    def __init__(self):
        """Initialize an empty CFG."""
        self.nodes = []                    # List of all CFGNode objects
        self.entry_node = None             # Entry node (start of program)
        self.exit_node = None              # Exit node (end of program)
        self.label_to_node = {}            # Mapping from label to CFGNode
    
    def add_node(self, node):
        """Add a node to the CFG."""
        if node not in self.nodes:
            self.nodes.append(node)
        if node.label is not None:
            self.label_to_node[node.label] = node
    
    def get_node_by_label(self, label):
        """Get a node by its label."""
        return self.label_to_node.get(label)
    
    def __repr__(self):
        return f"ControlFlowGraph({len(self.nodes)} nodes)"


def _get_node_description(ast_node):
    """
    Generate a human-readable description of an AST node.
    
    Args:
        ast_node: TreeNode from the AST
        
    Returns:
        String description of the node
    """
    if ast_node.type == ASSIGN:
        # Format: "x := expression"
        var_name = ast_node.children[0].value if ast_node.children else "?"
        rhs = (_reconstruct_expr_from_ast(ast_node.children[1])
               if ast_node.children else "?")
        return f"{var_name} := {rhs}"
    elif ast_node.type == SKIP:
        return "skip"
    elif ast_node.type in [WHILE, IF]:
        # For conditions, we'll use a generic description
        cond_expr = _reconstruct_expr_from_ast(ast_node)
        return f"{ast_node.type}: {cond_expr}"
    else:
        return str(ast_node.value) if ast_node.value else str(ast_node.type)

def _reconstruct_expr_from_ast(node):
    '''
    (Re-)construct an expression, such as 3, x + y, 2 * z, etc., from
    the root node for the expression in an AST. The root node for an
    integer value 3, e.g., would have type INT and a value of 3.
    The root node for the expression x + y would have a
    root node with type ADD and value '+', with two children for the
    expressions. The root node for an IF or WHILE loop has the
    condition information in the first child node.
    Returns "X" for unrecognized or incorrectly formatted nodes.
    '''
    if node.type in [INT, VAR]:
        return node.value
    elif node.type in [ADD, MULT, SUB]:
        op_symbol = node.value
        lhs = _reconstruct_expr_from_ast(node.children[0])
        rhs = _reconstruct_expr_from_ast(node.children[1])
        return f"{lhs} {op_symbol} {rhs}"
    elif node.type in [IF, WHILE]:
        condition_node = node.children[0]
        op_symbol = condition_node.value
        lhs = _reconstruct_expr_from_ast(condition_node.children[0])
        rhs = _reconstruct_expr_from_ast(condition_node.children[1])
        return f"{lhs} {op_symbol} {rhs}"
    else:
        return f"X"



def ast_to_cfg(ast_root):
    """
    Convert a decorated AST to a Control Flow Graph.
    
    Args:
        ast_root: Root TreeNode of the decorated AST
        
    Returns:
        ControlFlowGraph object
    """
    cfg = ControlFlowGraph()
    
    # Create entry and exit nodes
    entry_node = CFGNode(label=None, node_type='entry', content='ENTRY')
    exit_node = CFGNode(label=None, node_type='exit', content='EXIT')
    cfg.entry_node = entry_node
    cfg.exit_node = exit_node
    cfg.add_node(entry_node)
    cfg.add_node(exit_node)
    
    def process_statement(ast_node, current_chain_end):
        """
        Process an AST statement node and return the last CFG node in its chain.
        
        Args:
            ast_node: Current AST node to process
            current_chain_end: The last CFG node in the current chain (to connect to)
            
        Returns:
            The last CFG node in the processed chain
        """
        if ast_node is None:
            return current_chain_end
        
        # Handle sequence statements
        if ast_node.type == SEQ:
            chain_end = current_chain_end
            # Process each child in sequence
            for child in ast_node.children:
                chain_end = process_statement(child, chain_end)
            return chain_end
        
        # Handle assignment statements
        elif ast_node.type == ASSIGN:
            if ast_node.l is not None:
                # Create CFG node for this assignment
                content = _get_node_description(ast_node)
                cfg_node = CFGNode(
                    label=ast_node.l,
                    node_type='assign',
                    content=content,
                    ast_node=ast_node
                )
                cfg.add_node(cfg_node)
                
                # Connect to current chain
                if current_chain_end is not None:
                    current_chain_end.add_successor(cfg_node)
                
                return cfg_node
            else:
                # No label, skip (shouldn't happen after decoration)
                return current_chain_end
        
        # Handle skip statements
        elif ast_node.type == SKIP:
            if ast_node.l is not None:
                cfg_node = CFGNode(
                    label=ast_node.l,
                    node_type='skip',
                    content='skip',
                    ast_node=ast_node
                )
                cfg.add_node(cfg_node)
                
                if current_chain_end is not None:
                    current_chain_end.add_successor(cfg_node)
                
                return cfg_node
            else:
                return current_chain_end
        
        # Handle if-then-else statements
        elif ast_node.value == 'IF' or ast_node.type == IF:
            # The condition node has a label
            condition_node_ast = ast_node.children[0]  # condition
            true_block_ast = ast_node.children[1]      # then block
            else_block_ast = ast_node.children[2] if len(ast_node.children) > 2 else None  # else block
            
            # Create CFG node for condition
            if condition_node_ast.l is not None:
                condition = _get_node_description(ast_node)
                condition_cfg_node = CFGNode(
                    label=condition_node_ast.l,
                    node_type='condition',
                    content=f'{condition}',
                    ast_node=condition_node_ast
                )
                cfg.add_node(condition_cfg_node)
                
                # Connect to current chain
                if current_chain_end is not None:
                    current_chain_end.add_successor(condition_cfg_node)
            else:
                condition_cfg_node = current_chain_end
            
            # Process true branch
            true_end = process_statement(true_block_ast, None)
            
            # Process else branch
            else_end = process_statement(else_block_ast, None) if else_block_ast else None
            
            # Connect condition to branches (true and false)
            if true_end is not None:
                # Find the first node in the true branch
                true_start = true_end
                while true_start.predecessors:
                    pred = true_start.predecessors[0]
                    if pred == condition_cfg_node:
                        break
                    true_start = pred
                condition_cfg_node.add_successor(true_start)
            
            if else_end is not None:
                # Find the first node in the else branch
                else_start = else_end
                while else_start.predecessors:
                    pred = else_start.predecessors[0]
                    if pred == condition_cfg_node:
                        break
                    else_start = pred
                condition_cfg_node.add_successor(else_start)
            elif true_end is None:
                # Both branches empty - condition points to merge/exit
                pass
            
            # Create merge node (if needed)
            # If both branches exist, we need a merge point
            if true_end is not None and else_end is not None:
                merge_node = CFGNode(
                    label=None,
                    node_type='merge',
                    content='merge'
                )
                cfg.add_node(merge_node)
                true_end.add_successor(merge_node)
                else_end.add_successor(merge_node)
                return merge_node
            elif true_end is not None:
                return true_end
            elif else_end is not None:
                return else_end
            else:
                # Both branches are empty (shouldn't happen)
                return condition_cfg_node
        
        # Handle while-do statements
        elif ast_node.value == 'WHILE' or ast_node.type == WHILE:
            condition_node_ast = ast_node.children[0]  # condition
            while_block_ast = ast_node.children[1]     # do block
            
            # Create CFG node for condition
            if condition_node_ast.l is not None:
                condition = _get_node_description(ast_node)
                condition_cfg_node = CFGNode(
                    label=condition_node_ast.l,
                    node_type='condition',
                    content=f"{condition}",
                    ast_node=condition_node_ast
                )
                cfg.add_node(condition_cfg_node)
                
                # Connect to current chain
                if current_chain_end is not None:
                    current_chain_end.add_successor(condition_cfg_node)
            else:
                condition_cfg_node = current_chain_end
            
            # Process while body independently
            # We'll connect condition to body start and body end back to condition
            body_end = process_statement(while_block_ast, None)
            
            # Connect condition to body (true branch) and body back to condition (loop)
            if body_end is not None:
                # Find the first node in the body chain
                # The first node is the one with no predecessors (except possibly condition)
                body_start = body_end
                # Traverse backwards to find the first node
                while body_start.predecessors:
                    # Check if all predecessors are condition (shouldn't happen) or find the real first
                    all_are_condition = all(p == condition_cfg_node for p in body_start.predecessors)
                    if all_are_condition or len(body_start.predecessors) == 0:
                        break
                    # Get a predecessor that's not condition
                    for pred in body_start.predecessors:
                        if pred != condition_cfg_node:
                            body_start = pred
                            break
                    else:
                        break
                
                # Connect condition to body start (true branch)
                condition_cfg_node.add_successor(body_start)
                # Connect body end back to condition (loop back)
                body_end.add_successor(condition_cfg_node)
            else:
                # Empty body - condition's true branch points back to itself
                condition_cfg_node.add_successor(condition_cfg_node)
            
            # The condition node has two successors:
            # 1. Body start (if true) - connected above
            # 2. Exit (if false) - will be connected when we return from this function
            
            return condition_cfg_node
        
        # Unknown node type, skip
        return current_chain_end
    
    # Process the entire AST starting from entry
    last_node = process_statement(ast_root, cfg.entry_node)
    
    # Connect the last node to exit
    if last_node is not None:
        last_node.add_successor(cfg.exit_node)
    else:
        # If no nodes were created, connect entry directly to exit
        cfg.entry_node.add_successor(cfg.exit_node)
    
    return cfg


def generate_cfg_dot(cfg, filename="cfg.dot"):
    """
    Generate a Graphviz DOT file for visualizing the Control Flow Graph.
    
    Args:
        cfg: ControlFlowGraph object
        filename: Output filename for the DOT file
    """
    dot_content = ["digraph CFG {"]
    dot_content.append("    rankdir=TB;")  # Top to bottom layout
    dot_content.append("    node [shape=box, style=rounded];")
    dot_content.append("")
    
    # Add all nodes
    for node in cfg.nodes:
        if node.label is not None:
            label_str = f"{node.label}\\n{node.content}"
        else:
            label_str = node.content
        
        # Color code by node type
        if node.node_type == 'entry':
            color = "green"
        elif node.node_type == 'exit':
            color = "red"
        elif node.node_type == 'condition':
            color = "lightblue"
        elif node.node_type == 'merge':
            color = "yellow"
        else:
            color = "white"
        
        node_id = f"node_{node.label if node.label is not None else node.node_type}"
        dot_content.append(f'    "{node_id}" [label="{label_str}", fillcolor={color}, style="rounded,filled"];')
    
    dot_content.append("")
    
    # Add all edges
    for node in cfg.nodes:
        node_id = f"node_{node.label if node.label is not None else node.node_type}"
        for successor in node.successors:
            succ_id = f"node_{successor.label if successor.label is not None else successor.node_type}"
            dot_content.append(f'    "{node_id}" -> "{succ_id}";')
    
    dot_content.append("}")
    
    # Write to file
    with open(filename, "w") as f:
        f.write("\n".join(dot_content))
    
    print(f"CFG DOT file '{filename}' generated successfully!")
    print(f"CFG contains {len(cfg.nodes)} nodes.")


def print_cfg(cfg):
    """
    Print a text representation of the CFG for debugging.
    
    Args:
        cfg: ControlFlowGraph object
    """
    print("Control Flow Graph:")
    print("=" * 70)
    
    for node in cfg.nodes:
        label_str = f"Label {node.label}" if node.label is not None else node.node_type.upper()
        print(f"{label_str} ({node.node_type}): {node.content}")
        
        if node.successors:
            succ_labels = []
            for succ in node.successors:
                if succ.label is not None:
                    succ_labels.append(f"Label {succ.label}")
                else:
                    succ_labels.append(succ.node_type.upper())
            print(f"  -> {', '.join(succ_labels)}")
        print()
    
    print("=" * 70)

