{
    "start_symbol":"S",
    "rules": { "S":[["A"]],
               "A":[["B", "C"]],
               "B":[["D"], ["\u03B5"]],
               "C":[["E"]],
               "D":[["d"]],
               "E":[["\u03B5"]]},
    "terminals":["d"],
    "nonterminals":["S", "A", "B", "C", "D", "E"],
    "other":["\u03B5", "eof"]
}