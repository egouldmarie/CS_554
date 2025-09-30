from typing import NamedTuple
import time
import sys
import re

# Adapted from the tokenization example in the python docs for regular expressions
# https://docs.python.org/3/library/re.html#writing-a-tokenizer
class Token(NamedTuple):
    type: str
    value: str
    line: int
    column: int

def tokenize(code):
    # Reserved Keywords
    keywords = {"true", "false", "not", "skip", "if", "then", "else", "fi", "while", "do", "od"}
    # Regular Expressions identifying Tokens in our Language
    token_specification = [
        ("RPAR",       r"\("),                            # Right paranthesis
        ("LPAR",       r"\)"),                            # Left paranthesis
        ("RBRAC",      r"\["),                            # Right bracket
        ("LBRAC",      r"\]"),                            # Left bracket
        ("INTEGER",    r"0|([1-9])\d*"),                  # Integer
        ("VARIABLE",   r"[A-Za-z](\w|'|_)*"),             # Variables
        ("ASSIGN",     r":="),                            # Assignment
        ("SEQUENCING", r";"),                             # Command sequencing
        ("OP_A",       r'[+\-*]'),                        # Arithmetic operators
        ("OP_R",       r'=|<|<=|>=|>'),                   # Binary relational operators
        ("NEWLINE",    r'\n'),                            # Line endings
        ("IGNORE",     r"(--.*|\{-(.|\n|\r)*-\})|\s+"),   # ignore comments and white space
        ("MISMATCH",   r'.'),                             # Any other character
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    line_num = 1
    line_start = 0
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start
        if kind == 'INTEGER':
            value = int(value)
        elif kind == 'VARIABLE' and value in keywords:
            kind = value
        elif kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
            continue
        elif kind == 'IGNORE':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'{value!r} unexpected on line {line_num}')
        yield Token(kind, value, line_num, column)

if __name__ == "__main__":
    # read in file text
    file = open(sys.argv[1], "r")
    text = file.read()
    file.close()

    print(text)

    for token in tokenize(text):
        print(token)