import pytest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scanner import Tokenize


def test_bad_syntax():
    """
    Test that all files in the bad_syntax directory raise a RuntimeError
    when processed by the Tokenize function.
    """
    bad_syntax_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'bad_syntax')
    
    # Get all .while files in the bad_syntax directory
    bad_syntax_files = [f for f in os.listdir(bad_syntax_dir) if f.endswith('.while')]
    
    # Ensure we found some files to test
    assert len(bad_syntax_files) > 0, "No .while files found in bad_syntax directory"
    
    for filename in bad_syntax_files:
        filepath = os.path.join(bad_syntax_dir, filename)
        
        # Read the file content
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Test that Tokenize raises a RuntimeError
        try:
            list(Tokenize(content))
            pytest.fail(f"File {filename} with content '{content.strip()}' "
                       f"should have raised a RuntimeError but did not")
        except RuntimeError:
            pass

def test_good_syntax():
    """
    Test that all files in the good_syntax directory do not raise a RuntimeError
    when processed by the Tokenize function.
    """
    good_syntax_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'good_syntax')
    
    # Get all .while files in the bad_syntax_scanner directory
    good_syntax_files = [f for f in os.listdir(good_syntax_dir) if f.endswith('.while')]
    
    # Ensure we found some files to test
    assert len(good_syntax_files) > 0, "No .while files found in good_syntax directory"
    
    for filename in good_syntax_files:
        filepath = os.path.join(good_syntax_dir, filename)
        
        # Read the file content
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Test that Tokenize does NOT raise a RuntimeError for good syntax
        try:
            list(Tokenize(content))
            pass
        except RuntimeError as e:
            pytest.fail(f"File {filename} with content '{content.strip()}' "
                       f"raised an unexpected RuntimeError: {e}")