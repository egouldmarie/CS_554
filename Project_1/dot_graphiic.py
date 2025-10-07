
def generate_dot_from_tree(parse_tree):
    '''
    Given the parse_tree list [stmt1, stmt2, ..., stmtn] consisting
    of a list of (possibly nested) program statements, construct the
    corresponding DOT statements and eventual .dot file for
    visualization using Graphviz (https://graphviz.org/).
    Some of this code was guided by a Google search for converting
    a list of nested tuples into DOT language.

    Part of the challenge: the .dot file needs every node to have
    a unique id, and for us that unique id cannot depend on the
    content of the tuple on which a node is based because the
    same exact tuple can appear multiple times in different
    places in the tree --- for example, we might have an assignment
    tuple ("assign", ("var", "x"), ("int", 1)) representing the
    statement "x := 1", but such an assignment (and the subsequent
    tuple) can appear multiple times in the tree.

    Notice that each tuple is actually a sub-tree, and in the extreme
    case the sub-tree might simply be a leaf. Notice also that the
    number of children of a parent is not constant, so the initial
    branching of a sub-tree depends on the type of tuple. An "assign"
    tuple will have two children, but an if-then-else tuple will have
    three children.
    '''

    dot_statements = ["digraph G {"]
    node_counter = 0
    node_map = {}

    def traverse_and_add(node_data, parent_id = None):
        nonlocal node_counter
        node_value = node_data[0]

        if node_value not in node_map:
            node_id = f"node_{node_counter}"
            node_map[node_value]


    # finish the DOT statements
    dot_statements.append("}")

    # Write the constructed DOT statements to a .dot file
    filename = "tree.dot"
    with open(filename, "w") as f:
        f.write("\n".join(dot_statements))


