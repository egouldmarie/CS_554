def compute_first_sets(g):
    '''
    Compute the FIRST sets of each grammar symbol x in the provided
    grammar g, returning a dictionary of symbol-to-set key-value pairs.
    The grammar g is a dictionary of attributes, with g["rules"] itself
    being a dictionary providing the production rules.
    '''
    eps = "\u03B5" 
    first_sets = {}
    non_terminals = set(g["rules"].keys())
    terminals = set(g["terminals"])
    productions = g["rules"] # a dictionary

    # (1) FIRST(x) for x in the set of terminal symbols
    for t in g["terminals"]:
        first_sets[t] = {t}

    # (2) FIRST(x) for x being the empty str or EOF
    first_sets[eps] = {eps}
    first_sets["eof"] = {"eof"}

    # (3) Initialize empty sets for the FIRST sets of the nonterminals
    for x in g["nonterminals"]:
        first_sets[x] = set()

    first_sets_changed = True
    # fixed-point computation: continue processing until
    # we see no change in the FIRST sets being constructed
    while(first_sets_changed):
        
        first_sets_changed = False
        for nt in non_terminals:
            for production in productions[nt]:
                
                # Calculate FIRST(X) for each production nt -> alpha
                current_first_alpha = set()
                can_derive_eps = True
                
                for symbol in production:
                    if symbol in first_sets: # how can it NOT be?
                        # Add FIRST(symbol) to current_first_alpha,
                        # except for epsilon if symbol cannot derive epsilon
                        first_of_symbol = first_sets[symbol].copy()
                        first_of_symbol = first_of_symbol - {eps}
                        current_first_alpha.update(first_of_symbol) # essentially a UNION

                        if eps not in first_sets[symbol]:
                            can_derive_eps = False
                            # first symbol whose FIRST set does not contain eps
                            # so we stop processing the sequence alpha
                            break

                if can_derive_eps:
                    # this means all symbols in the sequence alpha
                    # could derive epsilon, so we add epsilon to the FIRST
                    current_first_alpha.add(eps)

                # Add current_first_alpha to FIRST(nt)
                if not current_first_alpha.issubset(first_sets[nt]):
                    # we have a change!
                    first_sets[nt].update(current_first_alpha)
                    first_sets_changed = True

    return first_sets