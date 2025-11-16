eps = "\u03B5"

grammar_1 = {
    "start_symbol":"E",
    "rules": { "E":[["number", "X"]],
               "X":[["E", "Y"], [eps]],
               "Y":[["+", "X"], ["*", "X"]]},
    "terminals":["number", "+", "*"],
    "nonterminals":["E", "X", "Y"],
    "other":[eps, "eof"]
}

grammar_2 = {
    "start_symbol":"S",
    "rules": { "S":[["A"]],
               "A":[["B", "C"]],
               "B":[["D"], [eps]],
               "C":[["E"]],
               "D":[["d"]],
               "E":[[eps]]},
    "terminals":["d"],
    "nonterminals":["S", "A", "B", "C", "D", "E"],
    "other":[eps, "eof"]
}

grammar_3 = {
    "start_symbol":"S",
    "rules": { "S":[["A", "B"]],
               "A":[["a"], [eps]],
               "B":[["b"]]},
    "terminals":["a", "b"],
    "nonterminals":["S", "A", "B"],
    "other":[eps, "eof"]
}

grammar_4 = {
    "start_symbol":"S",
    "rules": { "S":[["A", "B", "C"]],
               "A":[["a"], [eps]],
               "B":[["b"], [eps]],
               "C":[["c"]]},
    "terminals":["a", "b", "c"],
    "nonterminals":["S", "A", "B", "C"],
    "other":[eps, "eof"]
}

grammar_5 = {
    "start_symbol":"S",
    "rules": { "S":[["A", "B"]],
               "A":[["a"]],
               "B":[["b"]]},
    "terminals":["a", "b"],
    "nonterminals":["S", "A", "B"],
    "other":[eps, "eof"]
}

grammar_6 = {
    "start_symbol":"S",
    "rules": { "S":[["A", "B"]],
               "A":[["a"]],
               "B":[["b"], [eps]]},
    "terminals":["a", "b"],
    "nonterminals":["S", "A", "B"],
    "other":[eps, "eof"]
}

grammar_7 = {
    "start_symbol":"E",
    "rules": { "E":[["T", "E'"]],
               "E'":[["+", "T", "E'"], [eps]],
               "T":[["F", "T'"]],
               "T'":[["*", "F", "T'"], [eps]],
               "F":[["(", "E", ")"], ["id"]]},
    "terminals":["+", "*", "(", ")", "id", "eof"],
    "nonterminals":["E", "E'", "F", "T", "T'"],
    "other":[eps, "eof"]
}