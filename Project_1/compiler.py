import sys
import time
import argparse

from parser import Parser
from scanner import Tokenize
from codegen import RISC_V_CodeGenerator
from trees import (
    Tree, TreeNode, convert_nested_tuple_to_tree, generate_dot_from_tree)

if __name__ == "__main__":

    argparser = argparse.ArgumentParser()
    argparser.add_argument("filename",
                           help="filename")
    argparser.add_argument("-v", "--verbose", action="store_true",
                           help="increase output verbosity"
                           )
    args = argparser.parse_args()

    # read in file text
    file = open(args.filename, "r")
    whileCode = file.read()
    file.close()

    print("\nInput code:")
    print("-------------------------------------------------------------------")
    print(whileCode)
    print("-------------------------------------------------------------------")

    # ---text---> scanner --tokens-->
    print("\nGenerated tokens:")
    print("-------------------------------------------------------------------")
    tokens = []
    for token in Tokenize(whileCode):
        print(token)
        tokens.append(token)
    
    print("-------------------------------------------------------------------")

    # --tokens--> parser ----ast---->
    print("\nParse Tree:")
    print("-------------------------------------------------------------------")

    #ast = parseTokens(tokens)

    parser = Parser(tokens)
    parse_tree = parser.parse()
    print(f"{parse_tree}")
    print("-------------------------------------------------------------------")
    
    # generate_dot_from_tree(parse_tree)

    # Generate RISC-V assembly code
    print("\nRISC-V Assembly Code:")
    print("------------------------------------------------------------------------")
    codegen = RISC_V_CodeGenerator()
    assembly = codegen.generate(parse_tree)
    print(assembly)
    print("------------------------------------------------------------------------")
    
    # Save assembly to file
    output_file = sys.argv[1].replace('.while', '.s')
    with open(output_file, 'w') as f:
        f.write(assembly)
    print(f"\nAssembly code saved to: {output_file}")
    TreeNode._next_id = 0
    explicit_tree_root = convert_nested_tuple_to_tree(parse_tree)
    explicit_tree = Tree(explicit_tree_root)
    generate_dot_from_tree(explicit_tree.root)

    print(f"View the 'tree.dot' file in Graphviz or VSCode to see the "
           "resulting abstract syntax tree (AST).")

    print("\n")