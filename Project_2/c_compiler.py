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
from trees import (
    Tree, TreeNode,
    decorate_ast, insert_labels, generate_dot_from_tree,
    convert_nested_tuple_parse_tree_to_tree,
    convert_nested_tuple_ast_to_tree)

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

    ast_file = tree_path+file_name+"_ast_tree.dot"
    parse_file = tree_path+file_name+"_parse_tree.dot"
    decorated_ast_file = decorated_tree_path+file_name+"_ast_tree.dot"

    labeled_path = args.filename[:idx] + "labeled/"
    os.makedirs(os.path.dirname(labeled_path), exist_ok=True)

    labeled_source = labeled_path + args.filename[idx:]

    compile_path = args.filename[:idx] + "compiled/"
    os.makedirs(os.path.dirname(compile_path), exist_ok=True)

    compiled_file = (compile_path + args.filename[idx:]).replace(".while", "")
    risc_v_file = compiled_file + ".s"
    c_file_name = compiled_file + ".c"
    c_file_name_2 = compiled_file + "_2.c"

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
    # tba
    with open(c_file_name_2, 'w') as f:
        f.write(c_code)
    print(f"\nC code translation saved to: {c_file_name_2}")

    # ======================================== #
    # Generate, display, and save to .s file   #
    # the RISC-V assembly code                 #
    # ======================================== #
    codegen = RISC_V_CodeGenerator(function_name)
    assembly = codegen.generate(ast)
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

    # this part is probably best shifted over to the c_codegen.py
    # coding file now, since we are simply translating a WHILE
    # prog into C rather than running assembly from a c prog.

    # First, some helpful details and sub-strings
    num_vars = len(codegen.variables)
    printVars = " ".join(codegen.variables)
    printVals = ""
    for i in range(num_vars):
        printVals += (
                f"    printf(\"{codegen.variables[i]} = %lld \\n\", "
                f"(long long)var_array[{i}]);\n"
        )
    
    # Construct the C code as a Python string (to be printed to a file)
    c_code_2 = (
             "#include <stdio.h>\n"
          +  "#include <stdlib.h>\n"
          +  "\n"
          +  f"extern void {codegen.name}(int64_t *var_arr);\n"
          +  "\n"
          +  "int main(int argc, char *argv[]) {\n"
          +  "\n"
          +  "    // Check if correct num of args provided\n"
          + f"    if(argc != {num_vars + 1}) " + "{\n"
          + f'        printf("Executable requires {num_vars} arguments.\\n");\n'
          + f'        printf("Usage: <filename> {printVars}\\n");\n'
          +  "        return EXIT_FAILURE;\n"
          +  "    }\n"
          +  "\n"
          + f"    // Establish array to store the {num_vars} int values\n"
          + f"    int64_t var_array[{num_vars}];\n"
          +  "\n"
          +  "    // Initialize the values\n"
          + f"    for (int i = 0; i < {num_vars}; i++) " + "{\n"
          +  "        var_array[i] = atoll(argv[i + 1]);\n"
          +  "    }\n"
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

    # with open(c_file_name_2, 'w') as f:
    #     f.write(c_code_2)
    # print(f"\nC code saved to: {c_file_name_2}\n")

    # ======================================== #
    # Construct the associated C code file     #
    # ======================================== #

    # First, some helpful details and sub-strings
    num_vars = len(codegen.variables)
    printVars = " ".join(codegen.variables)
    printVals = ""
    for i in range(num_vars):
        printVals += (
                f"    printf(\"{codegen.variables[i]} = %lld \\n\", "
                f"(long long)var_array[{i}]);\n"
        )

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
          + f"    if(argc != {num_vars + 1}) " + "{\n"
          + f'        printf("Executable requires {num_vars} arguments.\\n");\n'
          + f'        printf("Usage: <filename> {printVars}\\n");\n'
          +  "        return EXIT_FAILURE;\n"
          +  "    }\n"
          +  "\n"
          + f"    // Establish array to store the {num_vars} int values\n"
          + f"    int64_t var_array[{num_vars}];\n"
          +  "\n"
          +  "    // Initialize the values\n"
          + f"    for (int i = 0; i < {num_vars}; i++) " + "{\n"
          +  "        var_array[i] = atoll(argv[i + 1]);\n"
          +  "    }\n"
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
