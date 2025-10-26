from typing import NamedTuple
import re

# Much of the scanner/tokenization code was adapted from the
# tokenization example in the python docs for regular expressions:
# https://docs.python.org/3/library/re.html#writing-a-tokenizer

class Token(NamedTuple):
    '''
    Token(type, value, line, column) represents a token generated in
    in the process of scanning the text of a program file, specifying
    the type (such as an operation, parenthesis, etc), its value (for
    example, the actual string or integer value), and its location
    (line and column number). 
    '''
    type: str
    value: str
    line: int
    column: int

def Tokenize(code):
    '''
    tokenize(code) uses regular expressions to categorize elements
    of supplied code text and yield associated Tokens consisting of
    ordered tuples specifying the type, value, and location of the
    tokenized elements.
    '''
    # Reserved Keywords
    keywords = {"true", "false", "not", "skip", "if", "then", "else",
                "fi", "while", "do", "od", "and", "or"}
    # Regular Expressions identifying Tokens in our Language
    token_specification = [
        ("newline",    r'\n'),                            # Line endings - MUST be first for proper line counting
        ("comment_block", r"\{-[\s\S]*?-\}"),             # Multi-line block comments
        ("comment_line", r"--.*"),                        # Single-line comments
        ("lpar",       r"\("),                            # Right parenthesis
        ("rpar",       r"\)"),                            # Left parenthesis
        ("lbrac",      r"\["),                            # Right bracket
        ("rbrac",      r"\]"),                            # Left bracket
        ("int",        r"0|([1-9])\d*"),                  # Integer
        ("var",        r"[A-Za-z][A-Za-z0-9_]*"),         # Variables (no quotes)
        ("assign",     r":="),                            # Assignment
        ("seq",        r";"),                             # Command sequencing
        ("op_a",       r'[+\-*]'),                        # Arithmetic operators
        ("op_r",       r'=|<=|<|>=|>'),                   # Binary relational operators
        ("ignore",     r"\s+"),                           # whitespace
        ("mismatch",   r'.'),                             # Any other character
    ]
    # create the 'master' regex:
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    line_num = 1
    line_start = 0
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start
        if kind == 'int':
            value = int(value)
        elif kind == 'var' and value in keywords:
            kind = value
        elif kind == 'newline':
            line_start = mo.end()
            line_num += 1
            continue
        elif kind in ['ignore', 'comment_line', 'comment_block']:
            # Count newlines within ignored tokens (comments, whitespace)
            newlines_in_value = value.count('\n')
            if newlines_in_value > 0:
                line_num += newlines_in_value
                # Update line_start to the end of the match
                line_start = mo.end()
            continue
        elif kind == 'mismatch':
            raise RuntimeError(f'{value!r} unexpected on line {line_num}')
        yield Token(kind, value, line_num, column)
