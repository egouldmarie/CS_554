def find_nullable_nonterminals(grammar):
    """
    Determines and returns the set of nullable non-terminals
    in a given context-free grammar.
    Args:
        grammar: A grammar in the form of a dictionary,
           where grammar["rules"] is itself a dictionary where keys
           are non-terminals (strings) and values are lists of
           production rules (lists of strings).
           The epsilon character eps = "\u03B5" represents the empty
           string.
    Returns:
        set: A set of nullable non-terminal symbols.
    """
    eps = "\u03B5"
    nullable = set()
    changed = True

    # Initial pass: Add non-terminals that directly derive epsilon
    for non_terminal, productions in grammar["rules"].items():
        for production in productions:
            if production == [eps] or production == ['']:
                nullable.add(non_terminal)
                break # No need to continue checking

    # Unlikely, but worth checking for shortcut:
    if nullable == set(grammar["nonterminals"]):
        return nullable

    while changed:
        changed = False
        for non_terminal, productions in grammar["rules"].items():
            if non_terminal in nullable:
                continue  # Already determined as nullable

            for production in productions:
                # A production is nullable if (and only if) all
                # its symbols are nullable.
                all_nullable_in_rhs = True
                for symbol in production:
                    if symbol in grammar["nonterminals"]:
                        if symbol not in nullable:
                            all_nullable_in_rhs = False
                            break
                    elif symbol in grammar["terminals"]:
                        all_nullable_in_rhs = False
                        break

                if all_nullable_in_rhs:
                    if non_terminal not in nullable:
                        nullable.add(non_terminal)
                        changed = True
                        # Found a nullable production for this
                        # non-terminal, so we can stop
                        break  

    return nullable