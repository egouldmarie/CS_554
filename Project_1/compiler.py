import sys
import time

from pda import parseTokens
from parser import Parser
from scanner import Tokenize

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

    ast = parseTokens(tokens)

    #parser = Parser(tokens)
    #parse_tree = parser.parse()
    #print(f"parse_tree: {parse_tree}")
    print("------------------------------------------------------------------------")
    
    print("\n")