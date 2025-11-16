{
    "start_symbol":"E",
    "rules": { "E":[["number", "X"]],
               "X":[["E", "Y"], ["\u03B5"]],
               "Y":[["+", "X"], ["*", "X"]]},
    "terminals":["number", "+", "*"],
    "nonterminals":["E", "X", "Y"],
    "other":["\u03B5", "eof"]
}