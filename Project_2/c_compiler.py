"""
filename:     c_compiler.py
authors:      Warren Craft
author note:  based on earlier work authored with project partners
              Jaime Gould & Qinghong Shao
created:      2025-11-23
last updated: 2025-11-23
description:  Coordinates actions of Scanner, Parser, and
              C_CodeGenerator classes for the compiling of a
              WHILE language programs into corresponding C programs.
              Code based on the compiler.py code previously
              developed with co-authors Jaime Gould & Qing Shao.
              Created for CS 554 (Compiler Construction) at UNM.
"""

import os
import argparse
import subprocess

from parser import Parser
from scanner import Tokenize
from codegen import RISC_V_CodeGenerator
from c_codegen import C_CodeGenerator
from trees import decorate_ast, insert_labels, generate_dot_from_tree
from cfg import ast_to_cfg, generate_cfg_dot

if __name__ == "__main__":

    # argparser specifications and initial arg processing
    argparser = argparse.ArgumentParser()
    argparser.add_argument("filename",
                           help="filename")
    argparser.add_argument("-v", "--verbose", action="store_true",
                           help="increase output verbosity"
                           )
    args = argparser.parse_args()

    # collect file & directory names
    file_name = args.filename.split('/')[-1].replace('.while', '')
    function_name = file_name.replace('-', '_').replace(' ', '')

    # generate names for misc constructed files, such as the
    # .s, .c, and .dot files
    idx = args.filename.rfind('/')+1

    tree_path = args.filename[:idx] + "trees/"
    os.makedirs(os.path.dirname(tree_path), exist_ok=True)

    decorated_tree_path = args.filename[:idx] + "trees/decorated/"
    os.makedirs(os.path.dirname(decorated_tree_path), exist_ok=True)

    cfg_path = args.filename[:idx] + "trees/cfg/"
    os.makedirs(os.path.dirname(cfg_path), exist_ok=True)

    ast_file = tree_path+file_name+"_ast_tree.dot"
    parse_file = tree_path+file_name+"_parse_tree.dot"
    decorated_ast_file = decorated_tree_path+file_name+"_ast_tree.dot"
    cfg_file = cfg_path+file_name+"_cfg.dot"

    labeled_path = args.filename[:idx] + "labeled/"
    os.makedirs(os.path.dirname(labeled_path), exist_ok=True)

    labeled_source = labeled_path + args.filename[idx:]

    compile_path = args.filename[:idx] + "compiled/"
    os.makedirs(os.path.dirname(compile_path), exist_ok=True)

    compiled_file = (compile_path + args.filename[idx:]).replace(".while", "")
    risc_v_file = compiled_file + ".s"
    c_file_name = compiled_file + ".c"
    # c_file_name_2 = compiled_file + "_2.c"
    # temporary convenient c_file_name_2 for dev and testing
    c_file_name_2 = "temp_generated.c"
    c_compiled_file_name_2 = "temp_generated"

    # read in file text
    with open(args.filename, "r") as f:
        whileCode = f.read()

    print("\nInput WHILE code:")
    print("-" * 70)
    print(whileCode)
    print("-" * 70)

    # ---text---> scanner --tokens-->
    print("\nGenerated tokens:")
    print("-" * 70)
    tokens = []
    for token in Tokenize(whileCode):
        print(token)
        tokens.append(token)

    print("-" * 70)

    # ================================ #
    #  Init a Parser with tokens       #
    # ================================ #
    parser = Parser(tokens)

    # ================================ #
    #  Generate and display the        #
    #  parse tree (PT) and abstract    #
    #  syntax tree (AST)               #
    # ================================ #
    parse_tree, ast = parser.parse()
    parse_tree = parse_tree.root
    ast = ast.root

    print("\nParse Tree (PT):")
    print("-" * 70)
    print(f"{parse_tree}")
    print("-" * 70)

    print("\nAbstract Syntax Tree (AST):")
    print("-" * 70)
    print(f"{ast}")
    print("-" * 70)
    print("\n")

    # ============================ #
    #  Generate graphic rep of PT  #
    # ============================ #

    generate_dot_from_tree(parse_tree, filename=parse_file)

    # ============================ #
    # Generate graphic rep of AST  #
    # ============================ #
    generate_dot_from_tree(ast, filename=ast_file)

    decorate_ast(ast)
    generate_dot_from_tree(ast, filename=decorated_ast_file)

    print(f"View the '.dot' files in Graphviz or VSCode to see the "
           "resulting abstract syntax tree (AST).")

    labeled_code = insert_labels(ast, whileCode)[0]
    print(labeled_code)
    with open(labeled_source, 'w') as f:
        f.write(labeled_code)
    print(f"\nLabeled code saved to: {labeled_source}\n")

    # ======================================== #
    # Generate Control Flow Graph (CFG)        #
    # ======================================== #
    print("\nGenerating Control Flow Graph (CFG)...")
    print("-" * 70)
    cfg = ast_to_cfg(ast)
    generate_cfg_dot(cfg, filename=cfg_file)
    print(f"CFG DOT file saved to: {cfg_file}")
    print(f"CFG contains {len(cfg.nodes)} nodes.")
    print("-" * 70)
    print()

    # ======================================== #
    # Generate, display, and save to .c file   #
    # the C code version of the WHILE program  #
    # ======================================== #
    c_codegen = C_CodeGenerator(function_name)
    c_code = c_codegen.generate_2(ast)
    print("\nC Code:")
    print("-" * 70)
    print(c_code)
    print("-" * 70)

    # save to its own .c file:
    with open(c_file_name_2, 'w') as f:
        f.write(c_code)
    print(f"\nC code translation saved to: {c_file_name_2}")
    
    try:
        subprocess.run(["gcc", "-o", c_compiled_file_name_2, c_file_name_2],
                       check=True, capture_output=True)
        print(f"Compiled C file successfully.\nExecutable saved to: "
              f"{c_compiled_file_name_2}\n")
    except Exception as the_exception:
        print("Unable to compile C file.\n")
        print(f"EXCEPTION: {the_exception}")
