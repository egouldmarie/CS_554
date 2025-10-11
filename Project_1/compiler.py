import sys
import time

# from pda import parseTokens
from parser import Parser
from scanner import Tokenize
from trees import (
    Tree, TreeNode, convert_nested_tuple_to_tree, generate_dot_from_tree)

if __name__ == "__main__":
    # read in file text
    file = open(sys.argv[1], "r")
    whileCode = file.read()
    file.close()

    print("\nInput code:")
    print("------------------------------------------------------------------------")
    print(whileCode)
    print("------------------------------------------------------------------------")

    # ---text---> scanner --tokens-->
    print("\nGenerated tokens:")
    print("------------------------------------------------------------------------")
    tokens = []
    for token in Tokenize(whileCode):
        print(token)
        tokens.append(token)
    
    print("------------------------------------------------------------------------")

    # --tokens--> parser ----ast---->
    print("\nParse Tree:")
    print("------------------------------------------------------------------------")

    #ast = parseTokens(tokens)

    parser = Parser(tokens)
    parse_tree = parser.parse()
    print(f"{parse_tree}")
    print("------------------------------------------------------------------------")
    
    TreeNode._next_id = 0
    explicit_tree_root = convert_nested_tuple_to_tree(parse_tree)
    explicit_tree = Tree(explicit_tree_root)
    generate_dot_from_tree(explicit_tree.root)

    print(f"Use the 'tree.dot' in Graphviz or VSCode to see the "
           "resulting abstract syntax tree (AST).")

    print("\n")