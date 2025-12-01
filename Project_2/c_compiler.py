"""
filename:     c_compiler.py
authors:      Warren Craft
author note:  based on earlier work authored with project partners
              Jaime Gould & Qinghong Shao
created:      2025-11-23
last updated: 2025-11-30
description:  Coordinates actions of Scanner, Parser, ASTToC_Generator,
              and CFGToC_Generator classes for the compiling of a
              WHILE language program into a corresponding C program.
              Code based on the compiler.py code previously
              developed with co-authors Jaime Gould & Qing Shao.
              Created for CS 554 (Compiler Construction) at UNM.
"""

import os
import argparse
import subprocess

from parser import Parser
from scanner import Tokenize
# from codegen import RISC_V_CodeGenerator
from c_codegen import ASTToC_Generator, CFGToC_Generator
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
    # c_file_name_2 = "temp_generated.c"
    c_gen_from_ast_filename = "c_gen_from_ast.c"

    # c_compiled_file_name_2 = "temp_generated"
    c_gen_from_ast_compiled_filename = "c_gen_from_ast"

    # filenames for C code generated from CFG
    c_gen_from_cfg_filename = "c_gen_from_cfg.c"
    c_gen_from_cfg_compiled_filename = "c_gen_from_cfg"



    # read in file text
    with open(args.filename, "r") as f:
        whileCode = f.read()

    print("\nSource WHILE code:")
    print("-" * 70)
    print(whileCode)
    print("-" * 70)

    # generate tokens (using scanner.py)
    if args.verbose:
        print("\nGenerated tokens:")
        print("-" * 70)
    tokens = []
    for token in Tokenize(whileCode):
        if args.verbose:
            print(token)
        tokens.append(token)
    if args.verbose:
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

    if args.verbose:
        print("\nParse Tree (PT):")
        print("-" * 70)
        print(f"{parse_tree}")
        print("-" * 70)

    if args.verbose:
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
    if args.verbose:
        print(labeled_code)
    with open(labeled_source, 'w') as f:
        f.write(labeled_code)
    print(f"\nLabeled code saved to: {labeled_source}\n")

    # ======================================== #
    # Generate Control Flow Graph (CFG)        #
    # ======================================== #
    print("\nGenerating Control Flow Graph (CFG)...")
    print("-" * 70)
    cfg, cfg_nodes = ast_to_cfg(ast)
    generate_cfg_dot(cfg_nodes, filename=cfg_file)
    print("-" * 70)
    print()

    # ======================================== #
    # Generate, display, and save to .c file   #
    # the AST-based C code version of the      #
    # WHILE program                            #
    # ======================================== #

    # USAGE: ASTToC_Generator(source_file, output_c_file)
    # source_file is the original .while file (given as an arg
    # when running compiler_ast_to_c.py);
    # output_c_file is the desired name of the resulting .c file
    # Neither is actively used in the cfg.py code EXCEPT to provide
    # info for header comments written in the eventual .c file.

    ast_to_c_codegen = ASTToC_Generator(args.filename, c_gen_from_ast_filename)
    c_code_from_ast = ast_to_c_codegen.generate(ast)

    print("\nC Code generated from AST:")
    print("-" * 70)
    print(c_code_from_ast)
    print("-" * 70)

    # save the ast-based C code to its own .c file:
    with open(c_gen_from_ast_filename, 'w') as f:
        f.write(c_code_from_ast)
    print(f"\nC code translation saved to: {c_gen_from_ast_filename}")
    
    # attempt to compile the resulting ast-based .c file
    try:
        subprocess.run(["gcc", "-o", c_gen_from_ast_compiled_filename,
                        c_gen_from_ast_filename],
                       check=True, capture_output=True)
        print(f"Successfully compiled {c_gen_from_ast_filename}"
              "\nExecutable saved to: "
              f"{c_gen_from_ast_compiled_filename}\n")
    except Exception as the_exception:
        print("Unable to compile C file.\n")
        print(f"EXCEPTION: {the_exception}")
    

    # ======================================== #
    # Generate, display, and save to .c file   #
    # the CFG-based C code version of the      #
    # WHILE program                            #
    # ======================================== #

    # USAGE: CFGToC_Generator(source_file, output_c_file)
    # source_file is the original .while file (given as an arg
    # when running compiler_ast_to_c.py);
    # output_c_file is the desired name of the resulting .c file
    # Neither is actively used in the cfg.py code EXCEPT to provide
    # info for header comments written in the eventual .c file.

    cfg_to_c_codegen = CFGToC_Generator(args.filename, c_gen_from_cfg_filename)
    c_code_from_cfg = cfg_to_c_codegen.generate(cfg_nodes)

    print("\nC Code generated from CFG:")
    print("-" * 70)
    print(c_code_from_cfg)
    print("-" * 70)

    # save the cfg-based C code to its own .c file:
    with open(c_gen_from_cfg_filename, 'w') as f:
        f.write(c_code_from_cfg)
    print(f"\nC code translation saved to: {c_gen_from_cfg_filename}")
    
    # attempt to compile the resulting cfg-based .c file
    try:
        subprocess.run(["gcc", "-o", c_gen_from_cfg_compiled_filename,
                        c_gen_from_cfg_filename],
                       check=True, capture_output=True)
        print(f"Successfully compiled {c_gen_from_cfg_filename}"
              "\nExecutable saved to: "
              f"{c_gen_from_cfg_compiled_filename}\n")
    except Exception as the_exception:
        print("Unable to compile C file.\n")
        print(f"EXCEPTION: {the_exception}")
