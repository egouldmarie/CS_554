Project 2 - Release 2 (v2.2)
================================
**Group:** The RaspberryPi's

**Members:** Jaime Gould, Qinghong Shao, Warren Craft

## Task List:
- [x] **Labelled Syntax:** implemented in v2.1
- [x] **Control Flow Graphs:** implemented in this release
- [x] **Code Generation:** implemented in this release
- [x] **Testing:** completed
- [x] **Performance Evaluation:** completed

## Included in TAR file:
1. Compiler Code (found in `code/`)
2. Example CFGs (`exampleCFGs.pdf`)
3. Virtual RISC-V code (found in `riscv/`)
4. Example `.while` files (found in `code/tests/good_syntax`)

## Test Run Results
| **`.while` program** | **input** | **output** | **expected result** |
| --- | --- | --- | ---- |
|`example1-factorial`|output = 0, x = 5, y = 0, z = 0|output = 120, x = 5, y = 0, z = 120|✅|
|`example1-factorial`|output = 0, x = 20, y = 0, z = 0|output = 2432902008176640000, x = 20, y = 0, z = 2432902008176640000|✅|
|`example6-collatz`|input = 1000, n = 0, output = 0, quot = 0, rem = 0, steps = 0|input = 1000, n = 376, output = 3, quot = 62, rem = 1, steps = 3 |✅|
|`example13-fibonacci`|90||✅|
|`primescounter`|100||✅|
|`primescounter`|1000||✅|
|`primescounter`|10000||✅|
|`veryveryverysimpleloop`|1000000000||✅|


## Performance Evaluation
| **`.while` program** | **input** | **v1 run time (sec)** | **v2.2 run time (sec)** |
| --- | --- | --- | --- |
|`example1-factorial`|5|0.004||
|`example1-factorial`|20|0.003||
|`example6-collatz`|1000|0.004||
|`example13-fibonacci`|90|0.004||
|`primescounter`|100|0.004||
|`primescounter`|1000|0.063||
|`primescounter`|10000|13.22||
|`veryveryverysimpleloop`|1000000000|17.186||

&Jlqou8^w$w8%sYG