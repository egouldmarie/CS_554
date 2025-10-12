

class TreeNode:
    '''
    TreeNode is a general node in a tree, with a node containing
    some data and an ordered list of the node's children (each of
    which will itself be a TreeNode). For our purposes, each node
    has default attributes id, type, value, and children, but one 
    can add attributes at initialization by using other kwargs.
    For example,

        TreeNode(type='if', data=[1, 2, 3])

    will create a TreeNode of type 'if' and default values for id,
    value, and children, but also add attribute 'data' containing
    an ordered list of three integers.
    The TreeNode class includes a class-level counter for unique ids,
    which can be reset externally using TreeNode._next_id = n to
    reset the initial id number to n. The unique id can be helpful
    in eventually converting a Tree to DOT code in a .dot file for
    visualization.
    '''

    # Class-level counter for unique IDs
    _next_id = 0

    def __init__(self, **kwargs):
        '''
        Initialize a TreeNode with default attributes plus any specific
        values or additional attributes specified by kwarg arguments.
        '''
        self.id = TreeNode._next_id
        TreeNode._next_id += 1
        self.type = None
        self.value = None
        self.children = []
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        # To facilitate printing and debugging.
        if self.children == []:
            return f"{self.value}"
        elif self.type == 'var':
            return f"{self.value}"
        return f"({self.value} --> {self.children})"

class Tree:
    '''
    Tree represents a tree of tree nodes and provides related methods.
    '''

    def __init__(self, root = None):
        self.root = root

    def __repr__(self):
        # To facilitate printing and debugging
        if self.root:
            return f"Tree(self.root.value)"
        return "Empty Tree"

    # Depth-First Traversals #

    def dfs_preorder_traversal(self, node):
        '''
        Depth-first pre-order traversal of the tree (or the sub-tree
        rooted at given node), visiting current node then recursively
        visiting all of its children. This is here primarily for
        testing and debugging, but could be modified to be more
        generally useful (by making it a generator, for example).
        '''
        if node is None:
            return
        print(f"({node.id}, {node.type}, {node.value})")
        for child in node.children:
            self.dfs_preorder_traversal(child)

# ================== #
# UTILITY Functions  #
# ================== #

def convert_nested_tuple_to_tree(nested_tuple):
    '''
    A recursive function to convert a nested tuple representation of
    a parse tree, such as:
        ('prog', ('assign', ('var', 'y'), ('var', 'x')),
                 ('assign', ('var', 'z'), ('int', 1)) )
    to a more explicit tree-with-nodes representation (which then
    is more easily converted to DOT language and stored in a .dot file
    for display using Graphviz).
    '''

    if not nested_tuple:
        return None

    # Interpret first element of a tuple as node's type.
    # A node's value may be more complicated.
    node_type = nested_tuple[0]

    # the remaining elements (if any) are the children,
    # which themselves might be nested tuples
    children_tuples = nested_tuple[1:]

    # A dictionary to facilitate the choice of a 'value' for each
    # node, which in turn will be used eventually as the label for
    # the node in DOT language and visualization process
    type_to_value = {
        'add':'+', 'assign':':=', 'if':'if', 'mult':'*', 'not':'not',
        'prog':'prog', 'seq':';', 'sub':'\u2014', 'while':'while',
        '<':'<', '>':'>', '<=':'<=', '>=':'>=', '=':'='
    }

    # Establish the current TreeNode
    current_node = TreeNode(type=node_type, value=type_to_value[node_type])

    # Then recursively convert and add children, with some
    # specialization for subsequent TreeNodes of various types.
    for child_tuple in children_tuples:
        if isinstance(child_tuple, tuple):
            # if child is a var or int type, treat it like a leaf
            if child_tuple[0] in ['var', 'int']:
                _type = child_tuple[0]
                _value = child_tuple[1]
                current_node.children.append(TreeNode(type=_type, value=_value))
            else:
                # if a child is some other nested tuple
                child_node = convert_nested_tuple_to_tree(child_tuple)
                if child_node:
                    current_node.children.append(child_node)
        elif isinstance(child_tuple, list):
            # a list corresponds to sequence of stmts inside a while
            # block, an if-true block, or if-else block.
            _type = 'seq'
            _value = type_to_value[_type]
            _child_node = TreeNode(type=_type, value=_value)
            for item in child_tuple:
                _child_node.children.append(convert_nested_tuple_to_tree(item))
            current_node.children.append(_child_node)
        else:
            # child is a 'leaf' value, not a tuple
            current_node.children.append(
                    TreeNode(type = child_tuple, value = child_tuple))

    return current_node

def generate_dot_from_tree(root_node, filename="tree.dot"):
    '''
    Given a Tree (consisting of a tree of TreeNodes), construct the
    DOT language output corresponding to an undirected graph and
    save the result in file 'filename.dot'. The resulting .dot file
    should be able to be interpreted by Graphviz or an extension in
    VSCode to visualize the graph.
    Labels for the graph visualization are taken from the 'value'
    attribute of each TreeNode.
    '''
    
    dot_content = ["digraph Tree {"]

    def _traverse_and_add_nodes(node):
        dot_content.append(f'    "{node.id}" [label="{node.value}"];')
        for child in node.children:
            dot_content.append(f'    "{node.id}" -> "{child.id}";')
            _traverse_and_add_nodes(child)

    _traverse_and_add_nodes(root_node)
    dot_content.append("}")

    with open(filename, "w") as f:
        f.write("\n".join(dot_content))

    print(f"\nDOT file '{filename}.dot' generated successfully!\n")