import sys
import time
import parser
import scanner
import importlib

importlib.reload(scanner)
importlib.reload(parser)

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
    for token in scanner.tokenize(whileCode):
        print(token)
        tokens.append(token)
    
    print("------------------------------------------------------------------------")

    # --tokens--> parser ----ast---->
    print("\nAbstract Syntax Tree:")
    print("------------------------------------------------------------------------")

    #ast = parser.parseTokens(tokens)

    prsr = parser.Parser(tokens)
    parse_tree = prsr.parse()
    print(f"parse_tree: {parse_tree}")
    print("------------------------------------------------------------------------")
    
    print("\n")