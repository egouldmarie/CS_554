"""
filename:     compiler.py
authors:      Jaime Gould, Qinghong Shao, Warren Craft
created:      2025-10-03
last updated: 2025-10-29
description:  Coordinates actions of Scanner, Parser, and
              RISC_V_CodeGenerator classes for the compiling of
              WHILE language programs, including the construction
              of bespoke C programs for each compiled WHILE program.
              Created for CS 554 (Compiler Construction) at UNM.
"""

import os
import argparse
import subprocess

from parser import Parser
from scanner import Tokenize
from codegen import RISC_V_CodeGenerator
from trees import decorate_ast, insert_labels, generate_dot_from_tree
from cfg import CFG
from optimizer import Optimizer

if __name__ == "__main__":

    argparser = argparse.ArgumentParser()
    argparser.add_argument("filename",
                           help="filename")
    argparser.add_argument("-v", "--verbose", action="store_true",
                           help="increase output verbosity"
                           )
    args = argparser.parse_args()

    # function, file, and directory names
    file_name = args.filename.split('/')[-1].replace('.while', '')
    function_name = file_name.replace('-', '_').replace(' ', '')

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
    cfg_optimized_file = cfg_path+file_name+"_optimized_cfg.dot"

    labeled_path = args.filename[:idx] + "labeled/"
    os.makedirs(os.path.dirname(labeled_path), exist_ok=True)

    labeled_source = labeled_path + args.filename[idx:]

    compile_path = args.filename[:idx] + "compiled/"
    os.makedirs(os.path.dirname(compile_path), exist_ok=True)

    compiled_file = (compile_path + args.filename[idx:]).replace(".while", "")
    risc_v_file = compiled_file + ".s"
    c_file_name = compiled_file + ".c"

    # read in file text
    with open(args.filename, "r") as f:
        whileCode = f.read()

    print("\nInput code:")
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
    cfg = CFG(ast)
    cfg.generate_cfg_dot(filename=cfg_file)
    print("-" * 70)
    print()

    # ======================================== #
    # Create and run optimizer                 #
    # (Live Variable Analysis)                 #
    # ======================================== #
    print("\nLive Analysis Equations:")
    print("-" * 70)
    optimizer = Optimizer(cfg)
    print("-" * 70)

    cfg.generate_cfg_dot(filename=cfg_optimized_file)

    # ======================================== #
    # Generate, display, and save to .s file   #
    # the RISC-V assembly code                 #
    # ======================================== #
    codegen = RISC_V_CodeGenerator(function_name)
    assembly = codegen.generate(cfg.nodes, optimizer)  # Generate from CFG instead of AST
    print("\nRISC-V Assembly Code:")
    print("-" * 70)
    print(assembly)
    print("-" * 70)

    # Save assembly to file
    with open(risc_v_file, 'w') as f:
        f.write(assembly)
    print(f"\nAssembly code saved to: {risc_v_file}")

    # ======================================== #
    # Construct the associated C code file     #
    # ======================================== #

    # First, some helpful details and sub-strings
    live_vars = optimizer.IN["entry"]
    num_live_vars = len(live_vars)
    num_vars = len(codegen.variables)
    printVars = " ".join(live_vars)
    printVals = ""
    for i in range(num_vars):
        printVals += (
                f"    printf(\"{codegen.variables[i]} = %lld \\n\", "
                f"(long long)var_array[{i}]);\n"
        )

    count = 1
    assignVals = ""
    for i in range(num_vars):
        if codegen.variables[i] in live_vars:
            assignVals += f"    var_array[{i}] = atoll(argv[{count}]);\n"
            count += 1
        else:
            assignVals += f"    var_array[{i}] = 0;\n"

    # Construct the C code as a Python string (to be printed to a file)
    c_code = (
             "#include <stdio.h>\n"
          +  "#include <stdlib.h>\n"
          +  "\n"
          +  f"extern void {codegen.name}(int64_t *var_arr);\n"
          +  "\n"
          +  "int main(int argc, char *argv[]) {\n"
          +  "\n"
          +  "    // Check if correct num of args provided\n"
          + f"    if(argc != {num_live_vars + 1}) " + "{\n"
          + f'        printf("Executable requires {num_live_vars} argument(s).\\n");\n'
          + f'        printf("Usage: <filename> {printVars}\\n");\n'
          +  "        return EXIT_FAILURE;\n"
          +  "    }\n"
          +  "\n"
          + f"    // Establish array to store the {num_vars} int values\n"
          + f"    int64_t var_array[{num_vars}];\n"
          +  "\n"
          +  "    // Initialize the values\n"
          + assignVals
          +  "\n"
          +  "    // Print initialized array values to verify:\n"
          +  '    printf("\\n");\n'
          +  '    printf("Initial variable values are: \\n");\n'
          + printVals
          +  "\n"
          +  f"    {codegen.name}(var_array);\n"
          +  "\n"
          +  "    // Print final array values:\n"
          +  '    printf("\\nFinal variable values are: \\n");\n'
          + printVals
          +  '    printf("\\n");\n'
          +  "\n"
          +  "    return EXIT_SUCCESS;\n"
          +  "}\n"
    )

    with open(c_file_name, 'w') as f:
        f.write(c_code)
    print(f"\nC code saved to: {c_file_name}\n")

    try:
        subprocess.run(["gcc", "-o", compiled_file, c_file_name, risc_v_file], check=True, capture_output=True)
        print(f"Compiled Assembly and C files successfully.\nExecutable saved to: {compiled_file}\n")
    except:
        print("Unable to compile Assembly and C files on this architecture.\n")
