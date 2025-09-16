'''
author: wdc
date  : 09/14/2025
Defines an interative factorial function and repeatedly calls the
function to compute n! for n in {0, 1, ..., 12}, 1 million times. 
This simple program was intended for use in exploring the (temporal)
performance difference between the b146-46.cs.unm.edu (b146) and
risc-machine-2.cs.unm.edu machines available at the UNM CS department,
for CS 554 (Compiler Construction). 
'''

import math
import time

def factorial(n):
    '''
    Returns n!, the factorial of non-negative integer n.
    '''

    if not isinstance(n, int) or n < 0:
        raise ValueError("Input must be a non-negative integer.")

    if n == 0 or n == 1:
        return 1

    result = 1
    for i in range(2, n + 1):
        result *= i

    return result


if __name__ == "__main__":

    start_time = time.time()

    temp_result = 0
    for i in range(0, 1000000):
        for i in range(0, 13):
            temp_result = factorial(i)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Run time: {elapsed_time:.4f} secs")


