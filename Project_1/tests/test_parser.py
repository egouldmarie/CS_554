import pytest
import os
import sys
import subprocess

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_bad_syntax():
    """
    Test that all files in the bad_syntax directory raise a RuntimeError
    when processed by the Tokenize function.
    """
    bad_syntax_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                  'examples', 'bad_syntax_parser')
    
    # Get all .while files in the bad_syntax_parser directory
    bad_syntax_files = [f for f in os.listdir(bad_syntax_dir) if f.endswith('.while')]
    assert len(bad_syntax_files) > 0, "No .while files found in bad_syntax directory"

    for filename in bad_syntax_files:
        filepath = os.path.join(bad_syntax_dir, filename)
        
        # Run the compiler.py script and capture output
        result = subprocess.run(['python', 'compiler.py', filepath],
                                capture_output=True, text=True)
        assert result.returncode != 0, f"File {filename} should have returned an error but did not."