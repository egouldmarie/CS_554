#!/usr/bin/env python3
"""
Compilation Performance Testing Script for WHILE Compiler
Tests compilation performance
"""

import os
import sys
import time
import subprocess
from datetime import datetime
from pathlib import Path


class CompilationTester:
    def __init__(self):
        self.test_dir = Path("performance_tests")
        self.test_dir.mkdir(exist_ok=True)

    def log(self, message):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")

    def test_compilation(self, while_file):
        """Test compilation performance"""
        self.log(f"Testing compilation of {while_file}")

        base_name = Path(while_file).stem

        # Measure compilation time
        start_time = time.perf_counter()
        try:
            result = subprocess.run([
                sys.executable, "compiler.py", while_file
            ], capture_output=True, text=True, timeout=30)
            compilation_time = time.perf_counter() - start_time
            compilation_success = result.returncode == 0
        except Exception as e:
            compilation_time = 0
            compilation_success = False
            result = type('obj', (object,), {'stderr': str(e)})()

        # Check generated files
        s_file = f"{base_name}.s"
        c_file = f"{base_name}.c"

        if not os.path.exists(s_file):
            s_file = f"examples/good_syntax/{base_name}.s"
        if not os.path.exists(c_file):
            c_file = f"examples/good_syntax/{base_name}.c"

        # Get file sizes and instruction count
        assembly_size = os.path.getsize(s_file) if os.path.exists(s_file) else 0
        c_size = os.path.getsize(c_file) if os.path.exists(c_file) else 0

        instruction_count = 0
        line_count = 0
        if os.path.exists(s_file):
            try:
                with open(s_file, 'r') as f:
                    content = f.read()
                lines = content.split('\n')
                line_count = len(lines)
                instructions = [line.strip() for line in lines
                                if line.strip() and not line.strip().startswith('#')
                                and not line.strip().startswith('.') and ':' not in line]
                instruction_count = len(instructions)
            except:
                instruction_count = 0
                line_count = 0

        return {
            "file": while_file,
            "compilation_success": compilation_success,
            "compilation_time": compilation_time,
            "assembly_size": assembly_size,
            "c_size": c_size,
            "instruction_count": instruction_count,
            "line_count": line_count,
            "error": result.stderr if not compilation_success else None
        }

    def run_tests(self):
        """Run compilation tests for both target files"""
        test_files = [
            "examples/good_syntax/example6-collatz.while",
            "examples/good_syntax/example13-fibonacci.while"
        ]

        results = []

        for test_file in test_files:
            if os.path.exists(test_file):
                result = self.test_compilation(test_file)
                results.append(result)
            else:
                print(f"Warning: {test_file} not found")

        return results

    def print_results(self, results):
        """Print formatted results"""
        print("\n" + "=" * 60)
        print("WHILE COMPILER COMPILATION PERFORMANCE RESULTS")
        print("=" * 60)
        print("Note: Execution testing skipped (RISC-V requires simulator)")
        print("=" * 60)

        for result in results:
            print(f"\nFile: {result['file']}")
            print("-" * 40)
            print(f"Compilation Success: {result['compilation_success']}")
            print(f"Compilation Time: {result['compilation_time']:.4f} seconds")
            print(f"Assembly Size: {result['assembly_size']} bytes")
            print(f"C Size: {result['c_size']} bytes")
            print(f"Total Lines: {result['line_count']}")
            print(f"Instruction Count: {result['instruction_count']}")

            if result['instruction_count'] > 0:
                efficiency = result['instruction_count'] / result['compilation_time']
                print(f"Compilation Efficiency: {efficiency:.2f} instructions/second")

            if result['error']:
                print(f"Error: {result['error'][:100]}...")

    def save_results(self, results):
        """Save results to file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        result_file = self.test_dir / f"compilation_results_{timestamp}.txt"

        with open(result_file, 'w') as f:
            f.write("WHILE COMPILER COMPILATION PERFORMANCE RESULTS\n")
            f.write(f"Generated: {datetime.now()}\n")
            f.write("Note: Execution testing skipped (RISC-V requires simulator)\n")
            f.write("=" * 50 + "\n\n")

            for result in results:
                f.write(f"File: {result['file']}\n")
                f.write(f"Compilation Success: {result['compilation_success']}\n")
                f.write(f"Compilation Time: {result['compilation_time']:.4f} seconds\n")
                f.write(f"Assembly Size: {result['assembly_size']} bytes\n")
                f.write(f"C Size: {result['c_size']} bytes\n")
                f.write(f"Total Lines: {result['line_count']}\n")
                f.write(f"Instruction Count: {result['instruction_count']}\n")
                if result['instruction_count'] > 0:
                    efficiency = result['instruction_count'] / result['compilation_time']
                    f.write(f"Compilation Efficiency: {efficiency:.2f} instructions/second\n")
                if result['error']:
                    f.write(f"Error: {result['error']}\n")
                f.write("\n")

        print(f"\nResults saved to: {result_file}")


def main():
    """Main function"""
    print("Compiler Compilation Performance Testing")

    tester = CompilationTester()

    # Check required files
    required_files = [
        "compiler.py",
        "examples/good_syntax/example6-collatz.while",
        "examples/good_syntax/example13-fibonacci.while"
    ]

    missing_files = [f for f in required_files if not os.path.exists(f)]
    if missing_files:
        print(f"Error: Missing files: {missing_files}")
        return 1

    # Run tests
    results = tester.run_tests()

    # Print results
    tester.print_results(results)

    # Save results
    tester.save_results(results)

    return 0


if __name__ == "__main__":
    sys.exit(main())
