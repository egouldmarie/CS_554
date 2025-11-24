from collections import defaultdict
from first_sets import compute_first_sets

def compute_follow_sets(g, verbose=False):
    '''
    Compute the FOLLOW sets of each non-terminal grammar symbol X in
    the provided grammar g, returning a dictionary of symbol-to-set
    key-value pairs. This implements the alg'm shown in Fig. 3.8 of
    Cooper & Torczon (2025), pg 109. In general, we are expecting a
    grammar object as a dictionary like this example:
    
            grammar = {
            "start_symbol":"E",
            "rules": { "E":[["number", "X"]], "X":[["E", "Y"], [eps]],
                       "Y":[["+", "X"], ["*", "X"]]},
            "terminals":["number", "+", "*"],
            "nonterminals":["E", "X", "Y"],
            "other":[eps, "eof"]
            }
    Args:
        g: A grammar in the form of a dictionary, where g["rules"] is a
           dictionary where keys are non-terminals (strings) and values
           are lists of production rules (lists of strings). The
           epsilon character eps = "\u03B5" represents the empty string.
    Returns:
        follow_sets: A dictionary of symbol-to-set key-value pairs
           giving the FOLLOW set for each non-terminal symbol. 
    '''

    # some initial conveniences
    eps = "\u03B5"
    start_symbol = g["start_symbol"]
    productions = g["rules"] # a dictionary
    non_terminals = g["nonterminals"] # list

    # (1) Compute FIRST sets using external fxn
    first_sets = compute_first_sets(g)

    # (2) Use Python's defaultdict() specialized dict subclass
    #     and initialize FOLLOW(X) for each non-terminal X
    follow_sets = defaultdict(set)
    for non_terminal in non_terminals:
        follow_sets[non_terminal] = set()

    # (3) Add "eof" to FOLLOW set of the start symbol
    follow_sets[start_symbol].add("eof")

    # (4) Iterate until FOLLOW sets don't change
    follow_sets_changed = True
    iter_count = 0
    while follow_sets_changed:

        follow_sets_changed = False
        for non_terminal in productions:
            for rhs in productions[non_terminal]:
                trailer = follow_sets[non_terminal]
                for i in range(len(rhs)-1, -1, -1):
                    symbol = rhs[i]
                    if symbol in non_terminals:
                        if follow_sets[symbol] != follow_sets[symbol].union(trailer):
                            follow_sets[symbol] = follow_sets[symbol].union(trailer)
                            follow_sets_changed = True
                        if eps in first_sets[symbol]:
                            trailer = trailer.union(first_sets[symbol]-{eps})
                        else:
                            trailer = first_sets[symbol]
                    else:
                        trailer = {symbol}
            
    return follow_sets