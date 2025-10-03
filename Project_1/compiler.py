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
    tokens = scanner.tokenize(whileCode)

    #print("\nGenerated tokens:")
    #print("------------------------------------------------------------------------")
    #for token in tokens:
    #    print(token)
    #print("------------------------------------------------------------------------")

    # --tokens--> parser ----ast---->
    ast = parser.parseTokens(tokens)

    #print("\nAbstract Syntax Tree:")
    #print("------------------------------------------------------------------------")
    #print("------------------------------------------------------------------------")