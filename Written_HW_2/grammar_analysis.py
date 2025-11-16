"""
filename:     grammar_analysis.py
authors:      Warren Craft
created:      2025-11-08
last updated: 2025-11-15
description:  Coordinates actions of Scanner, Parser, and
              RISC_V_CodeGenerator classes for the compiling of
              WHILE language programs, including the construction
              of bespoke C programs for each compiled WHILE program.
              Created for CS 554 (Compiler Construction) at UNM.
"""

import os
import argparse
import subprocess

import ast

from nullable import find_nullable_nonterminals
from first_sets import compute_first_sets
from follow_sets import compute_follow_sets

if __name__ == "__main__":

    argparser = argparse.ArgumentParser()
    argparser.add_argument("filename",
                           help="filename")
    argparser.add_argument("-v", "--verbose", action="store_true",
                           help="increase output verbosity"
                           )
    args = argparser.parse_args()

    # a grammar expected in args.filename

    # read in file text
    with open(args.filename, "r") as f:
        grammar_string = f.read()
        grammar = ast.literal_eval(grammar_string)

    print("\nGrammar:")
    print("-" * 70)
    for key, value in grammar.items():
        print(f"{key} : {value}")
    print("-" * 70)

    # ================================ #
    #  Determine and display the set   #
    #  of nullable non-terminals       #
    # ================================ #
    nullables = find_nullable_nonterminals(grammar)
    print("\nNullables:")
    print("-" * 70)
    print(nullables)
    print("-" * 70)
    print()

    # ================================ #
    #  Determine and display the       #
    #  FIRST sets of grammar symbols   #
    # ================================ #
    first_sets = compute_first_sets(grammar)
    print("FIRST sets:")
    print("-" * 70)
    for key, value in first_sets.items():
        print(f"{key} : {value}")
    print("-" * 70)
    print()

    # ================================ #
    #  Determine and display the       #
    #  FOLLOW sets of NT symbols       #
    # ================================ #
    follow_sets = compute_follow_sets(grammar)
    print("FOLLOW sets:")
    print("-" * 70)
    for key, value in follow_sets.items():
        print(f"{key} : {value}")
    print("-" * 70)
    print()
    
