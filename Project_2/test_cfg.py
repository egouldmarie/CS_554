"""
Test script for CFG module
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scanner import Tokenize
from parser import Parser
from trees import decorate_ast, TreeNode
from cfg import ast_to_cfg, generate_cfg_dot, print_cfg

def test_cfg_simple():
    """Test CFG generation with a simple assignment program"""
    print("=" * 70)
    print("Test 1: Simple Assignment")
    print("=" * 70)
    
    # Simple program: x := 5
    while_code = "x := 5"
    
    print(f"\nInput code:\n{while_code}\n")
    
    # Tokenize
    tokens = list(Tokenize(while_code))
    print("Tokens:", tokens)
    
    # Parse
    parser = Parser(tokens)
    parse_tree, ast = parser.parse()
    ast = ast.root
    
    # Decorate AST
    TreeNode._next_id = 0
    decorate_ast(ast)
    
    print("\nDecorated AST labels:")
    def print_labels(node, indent=0):
        if node.l is not None:
            print("  " * indent + f"Label {node.l}: {node.type} - {node.value}")
        for child in node.children:
            print_labels(child, indent + 1)
    print_labels(ast)
    
    # Generate CFG
    cfg = ast_to_cfg(ast)
    
    print("\n" + "=" * 70)
    print("CFG Structure:")
    print("=" * 70)
    print_cfg(cfg)
    
    # Generate DOT file
    generate_cfg_dot(cfg, "test_simple_cfg.dot")
    print("\nCFG DOT file saved to: test_simple_cfg.dot")
    
    return cfg

def test_cfg_sequence():
    """Test CFG generation with a sequence of assignments"""
    print("\n" + "=" * 70)
    print("Test 2: Sequence of Assignments")
    print("=" * 70)
    
    # Program: x := 1; y := 2; z := 3
    while_code = "x := 1; y := 2; z := 3"
    
    print(f"\nInput code:\n{while_code}\n")
    
    # Tokenize and parse
    tokens = list(Tokenize(while_code))
    parser = Parser(tokens)
    parse_tree, ast = parser.parse()
    ast = ast.root
    
    # Decorate AST
    TreeNode._next_id = 0
    decorate_ast(ast)
    
    # Generate CFG
    cfg = ast_to_cfg(ast)
    
    print("\n" + "=" * 70)
    print("CFG Structure:")
    print("=" * 70)
    print_cfg(cfg)
    
    # Generate DOT file
    generate_cfg_dot(cfg, "test_sequence_cfg.dot")
    print("\nCFG DOT file saved to: test_sequence_cfg.dot")
    
    return cfg

def test_cfg_if():
    """Test CFG generation with if-then-else"""
    print("\n" + "=" * 70)
    print("Test 3: If-Then-Else Statement")
    print("=" * 70)
    
    # Program: if x > 0 then y := 1 else y := 0 fi
    while_code = "if x > 0 then y := 1 else y := 0 fi"
    
    print(f"\nInput code:\n{while_code}\n")
    
    # Tokenize and parse
    tokens = list(Tokenize(while_code))
    parser = Parser(tokens)
    parse_tree, ast = parser.parse()
    ast = ast.root
    
    # Decorate AST
    TreeNode._next_id = 0
    decorate_ast(ast)
    
    # Generate CFG
    cfg = ast_to_cfg(ast)
    
    print("\n" + "=" * 70)
    print("CFG Structure:")
    print("=" * 70)
    print_cfg(cfg)
    
    # Generate DOT file
    generate_cfg_dot(cfg, "test_if_cfg.dot")
    print("\nCFG DOT file saved to: test_if_cfg.dot")
    
    return cfg

def test_cfg_while():
    """Test CFG generation with while loop"""
    print("\n" + "=" * 70)
    print("Test 4: While Loop")
    print("=" * 70)
    
    # Program: while x > 0 do x := x - 1 od
    while_code = "while x > 0 do x := x - 1 od"
    
    print(f"\nInput code:\n{while_code}\n")
    
    # Tokenize and parse
    tokens = list(Tokenize(while_code))
    parser = Parser(tokens)
    parse_tree, ast = parser.parse()
    ast = ast.root
    
    # Decorate AST
    TreeNode._next_id = 0
    decorate_ast(ast)
    
    # Generate CFG
    cfg = ast_to_cfg(ast)
    
    print("\n" + "=" * 70)
    print("CFG Structure:")
    print("=" * 70)
    print_cfg(cfg)
    
    # Generate DOT file
    generate_cfg_dot(cfg, "test_while_cfg.dot")
    print("\nCFG DOT file saved to: test_while_cfg.dot")
    
    return cfg

def test_cfg_factorial():
    """Test CFG generation with factorial program"""
    print("\n" + "=" * 70)
    print("Test 5: Factorial Program")
    print("=" * 70)
    
    # Read the factorial program
    with open("tests/good_syntax/example1-factorial.while", "r") as f:
        while_code = f.read()
    
    print(f"\nInput code:\n{while_code}\n")
    
    # Tokenize and parse
    tokens = list(Tokenize(while_code))
    parser = Parser(tokens)
    parse_tree, ast = parser.parse()
    ast = ast.root
    
    # Decorate AST
    TreeNode._next_id = 0
    decorate_ast(ast)
    
    # Generate CFG
    cfg = ast_to_cfg(ast)
    
    print("\n" + "=" * 70)
    print("CFG Structure:")
    print("=" * 70)
    print_cfg(cfg)
    
    # Generate DOT file
    generate_cfg_dot(cfg, "test_factorial_cfg.dot")
    print("\nCFG DOT file saved to: test_factorial_cfg.dot")
    
    return cfg

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("CFG Module Test Suite")
    print("=" * 70)
    
    try:
        # Run tests
        test_cfg_simple()
        test_cfg_sequence()
        test_cfg_if()
        test_cfg_while()
        test_cfg_factorial()
        
        print("\n" + "=" * 70)
        print("All tests completed!")
        print("=" * 70)
        print("\nGenerated DOT files:")
        print("  - test_simple_cfg.dot")
        print("  - test_sequence_cfg.dot")
        print("  - test_if_cfg.dot")
        print("  - test_while_cfg.dot")
        print("  - test_factorial_cfg.dot")
        print("\nYou can view these files in Graphviz or VSCode with Graphviz extension.")
        
    except Exception as e:
        print(f"\nError during testing: {e}")
        import traceback
        traceback.print_exc()

