import sys

from parser import Parser
from scanner import Tokenize
from codegen import RISC_V_CodeGenerator

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
    print("\nAbstract Syntax Tree:")
    print("------------------------------------------------------------------------")

    #ast = parseTokens(tokens)

    parser = Parser(tokens)
    parse_tree = parser.parse()
    print(f"parse_tree: {parse_tree}")
    print("------------------------------------------------------------------------")
    
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

    print("\n")