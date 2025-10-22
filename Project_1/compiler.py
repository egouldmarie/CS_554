import sys
import time
import argparse

from parser import Parser
from scanner import Tokenize
from codegen import RISC_V_CodeGenerator
from trees import (
    Tree, TreeNode, generate_dot_from_tree,
    convert_nested_tuple_parse_tree_to_tree,
    convert_nested_tuple_ast_to_tree)

if __name__ == "__main__":

    argparser = argparse.ArgumentParser()
    argparser.add_argument("filename",
                           help="filename")
    argparser.add_argument("-v", "--verbose", action="store_true",
                           help="increase output verbosity"
                           )
    args = argparser.parse_args()

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
    TreeNode._next_id = 0
    explicit_parse_tree_root = (
            convert_nested_tuple_parse_tree_to_tree(parse_tree))
    explicit_parse_tree = Tree(explicit_parse_tree_root)
    generate_dot_from_tree(
            explicit_parse_tree.root, filename='parse_tree.dot')

    # ============================ #
    # Generate graphic rep of AST  #
    # ============================ #
    TreeNode._next_id = 0  # reset id numbering to keep ids small
    explicit_ast_root = convert_nested_tuple_ast_to_tree(ast)
    explicit_ast = Tree(explicit_ast_root)
    generate_dot_from_tree(explicit_ast.root, filename='ast_tree.dot')
    print(f"View the '.dot' files in Graphviz or VSCode to see the "
           "resulting abstract syntax tree (AST).")

    # ======================================== #
    # Generate, display, and save to .s file   #
    # the RISC-V assembly code                 #
    # ======================================== #
    function_name = args.filename.split('/')[-1].replace('.while', '').replace('-', '_').replace('\w', '')
    codegen = RISC_V_CodeGenerator(function_name)
    assembly = codegen.generate(ast[1])
    print("\nRISC-V Assembly Code:")
    print("-" * 70)
    print(assembly)
    print("-" * 70)
    
    # Save assembly to file
    output_file = args.filename.replace('.while', '.s')
    with open(output_file, 'w') as f:
        f.write(assembly)
    print(f"\nAssembly code saved to: {output_file}")
    
    # ======================================== #
    # Construct the associated C code file     #
    # ======================================== #
    # this might be included in the codegen.py eventually
    # instead of here in compiler.py
    num_vars = len(codegen.variables)
    printVals = ""
    for i in range(num_vars):
        printVals += f"    printf(\"{codegen.variables[i]} = %lld \\n\", (long long)var_array[{i}]);\n"

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
          + f'        printf("Need {num_vars} args.");\n'
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

    # // Initialize the array using a for loop
    # for (int i = 0; i < 5; i++) {
    #     my_array[i] = (long long)i * 100; // Example: assign values 0, 100, 200, 300, 400
    # }

    c_file_name = args.filename.replace('.while', '.c')
    with open(c_file_name, 'w') as f:
        f.write(c_code)
    print(f"\nC code saved to: {c_file_name}")

    print("\n")