# Overview
**Author: Nathan J. Rowe**
*Email: nrowe1@unm.edu*
Week 3 Emulator Warmup in C for CS554 - Compiler Construction

`instructions.h` contains the functions for opcodes that do not handle array manipulations.
The array collection, execution loop, file parsing, and array-manipulating opcodes are handled in `um.c`

`um.c` is the main program for the emulator
`assembler.c` is the main program for the assembler
`disassembler.c` is the main program for the disassembler (I know these are very creative)
# How to Build
1. Extract with `tar -xvf nrowe1-um.tar`
2. Traverse to the extracted directory `cd cs554_um_nrowe1`
3. Build the compiler with `gcc -Wall -O2 um.c -o um`
4. Build the assembler with `gcc -Wall -O2 assembler.c -o uma`
5. Build the disassembler with `gcc -Wall -O2 assembler.c -o umd` 

*Note: The assembler and disassembler use headers provided by glibc, making them unavailable for compilation on Windows*

# Running the Assembler
The assembler takes a single filepath as input. The file must have a `.uma` extension. The assembler will save the resulting binary to `<filename>.um` in the current working directory.

Example: `./uma helloworld.uma`

## Assembler Results
*Note: The assembler is incomplete. Notably, a symbol table has yet to be implemented. This means there is no support for labels*

**INPUT**
```helloworld.uma

;; printing Hello world!

loadimm 0 72
out 0
loadimm 0 101
out 0
loadimm 0 108
out 0
loadimm 0 108
out 0
loadimm 0 111
out 0
loadimm 0 32
out 0
loadimm 0 119
out 0
loadimm 0 111
out 0
loadimm 0 114
out 0
loadimm 0 108
out 0
loadimm 0 100
out 0
loadimm 0 33
out 0 
loadimm 0 10
out 0

halt

```

**Execution Trace of output file**
```
nrowe1@b146-46:~/cs554/cs554_um_nrowe1$ date
Wed Aug 27 10:00:33 PM MDT 2025
nrowe1@b146-46:~/cs554/cs554_um_nrowe1$ gcc assembler.c -o uma
nrowe1@b146-46:~/cs554/cs554_um_nrowe1$ ./uma helloworld.uma
nrowe1@b146-46:~/cs554/cs554_um_nrowe1$ ./um helloworld.um
Hello world!
```

# Running the Disassembler
The disassembler takes a single filepath as input. The file must have a `.um` extension. The disassembler will save the resulting output to `<filename>.uma` in the current working directory.

## Disassembler Results
1. `./umd helloworld.uma`
```
nrowe1@b146-46:~/cs554/cs554_um_nrowe1$ date
Wed Aug 27 10:03:54 PM MDT 2025
nrowe1@b146-46:~/cs554/cs554_um_nrowe1$ gcc disassembler.c -o umd
nrowe1@b146-46:~/cs554/cs554_um_nrowe1$ ./umd helloworld.um
Disassembly complete. Output written to /nfs/student/student/n/nrowe1/cs554/cs554_um_nrowe1/helloworld.uma

nrowe1@b146-46:~/cs554/cs554_um_nrowe1$ cat helloworld.uma
loadimm R0 <- 72
out R0
loadimm R0 <- 101
out R0
loadimm R0 <- 108
out R0
loadimm R0 <- 108
out R0
loadimm R0 <- 111
out R0
loadimm R0 <- 32
out R0
loadimm R0 <- 119
out R0
loadimm R0 <- 111
out R0
loadimm R0 <- 114
out R0
loadimm R0 <- 108
out R0
loadimm R0 <- 100
out R0
loadimm R0 <- 33
out R0
loadimm R0 <- 10
out R0
halt

```
2. `./umd square.um`
```
nrowe1@b146-46:~/cs554/cs554_um_nrowe1$ ./umd square.um
Disassembly complete. Output written to /nfs/student/student/n/nrowe1/cs554/cs554_um_nrowe1/square.uma

nrowe1@b146-46:~/cs554/cs554_um_nrowe1$ cat square.uma
loadimm R0 <- 0
loadimm R1 <- 1
loadimm R5 <- 4
alloc [1][5], R2=1
loadimm R7 <- 8
aupd [R2][R1] <- R7
loadimm R4 <- 292
loadprog [0] <- [R0], PC=R4
halt
loadimm R6 <- 3
aidx R6 <- [R2][R6]
nand R6 <- R6,R6
add R6 <- R6,R1
loadimm R7 <- 2
aidx R7 <- [R2][R7]
add R6 <- R6,R7
loadimm R7 <- 4
aupd [R2][R7] <- R6
aidx R4 <- [R2][R1]
loadprog [0] <- [R0], PC=R4
loadimm R5 <- 5
alloc [2][5], R6=2
aupd [R6][R0] <- R2
loadimm R7 <- 36
aupd [R6][R1] <- R7
loadimm R5 <- 2
aidx R7 <- [R2][R5]
loadimm R5 <- 2
aupd [R6][R5] <- R7
loadimm R5 <- 3
aidx R7 <- [R2][R5]
loadimm R5 <- 3
aupd [R6][R5] <- R7
loadimm R4 <- 9
cmovnz R2 <- R6 if R1 != 0
loadprog [0] <- [R0], PC=R4
aidx R6 <- [R2][R0]
loadimm R7 <- 4
aidx R7 <- [R2][R7]
dealloc R2
cmovnz R2 <- R6 if R1 != 0
cmovnz R6 <- R1 if R1 != 0
cmovnz R6 <- R0 if R7 != 0
loadimm R7 <- 4
aupd [R2][R7] <- R6
aidx R4 <- [R2][R1]
loadprog [0] <- [R0], PC=R4
loadimm R5 <- 3
aupd [R2][R5] <- R0
in R6
loadimm R5 <- 4
aupd [R2][R5] <- R6
loadimm R5 <- 5
alloc [3][5], R6=3
aupd [R6][R0] <- R2
loadimm R7 <- 67
aupd [R6][R1] <- R7
loadimm R5 <- 4
aidx R7 <- [R2][R5]
loadimm R5 <- 2
aupd [R6][R5] <- R7
loadimm R7 <- 10
loadimm R5 <- 3
aupd [R6][R5] <- R7
loadimm R4 <- 20
cmovnz R2 <- R6 if R1 != 0
loadprog [0] <- [R0], PC=R4
aidx R6 <- [R2][R0]
loadimm R5 <- 4
aidx R7 <- [R2][R5]
loadimm R5 <- 5
aupd [R6][R5] <- R7
dealloc R2
cmovnz R2 <- R6 if R1 != 0
loadimm R5 <- 5
aidx R7 <- [R2][R5]
loadimm R4 <- 80
loadimm R5 <- 117
cmovnz R4 <- R5 if R7 != 0
loadprog [0] <- [R0], PC=R4
loadimm R5 <- 3
aidx R6 <- [R2][R5]
loadimm R7 <- 10
mul R6 <- R6,R7
loadimm R5 <- 6
aupd [R2][R5] <- R6
loadimm R5 <- 5
alloc [4][5], R6=4
aupd [R6][R0] <- R2
loadimm R7 <- 101
aupd [R6][R1] <- R7
loadimm R5 <- 4
aidx R7 <- [R2][R5]
loadimm R5 <- 2
aupd [R6][R5] <- R7
loadimm R7 <- 48
loadimm R5 <- 3
aupd [R6][R5] <- R7
loadimm R4 <- 9
cmovnz R2 <- R6 if R1 != 0
loadprog [0] <- [R0], PC=R4
aidx R6 <- [R2][R0]
loadimm R5 <- 4
aidx R7 <- [R2][R5]
loadimm R5 <- 7
aupd [R6][R5] <- R7
dealloc R2
cmovnz R2 <- R6 if R1 != 0
loadimm R5 <- 6
aidx R6 <- [R2][R5]
loadimm R5 <- 7
aidx R7 <- [R2][R5]
add R6 <- R6,R7
loadimm R5 <- 3
aupd [R2][R5] <- R6
loadimm R4 <- 49
loadprog [0] <- [R0], PC=R4
loadimm R5 <- 3
aidx R6 <- [R2][R5]
loadimm R5 <- 2
aupd [R2][R5] <- R6
aidx R4 <- [R2][R1]
loadprog [0] <- [R0], PC=R4
loadimm R5 <- 2
aidx R6 <- [R2][R5]
loadimm R5 <- 3
aupd [R2][R5] <- R6
loadimm R5 <- 3
aidx R6 <- [R2][R5]
loadimm R7 <- 10
div R6 <- R6,R7
loadimm R5 <- 4
aupd [R2][R5] <- R6
loadimm R5 <- 4
aidx R6 <- [R2][R5]
loadimm R7 <- 10
mul R6 <- R6,R7
loadimm R5 <- 7
aupd [R2][R5] <- R6
loadimm R5 <- 5
alloc [5][5], R6=5
aupd [R6][R0] <- R2
loadimm R7 <- 155
aupd [R6][R1] <- R7
loadimm R5 <- 3
aidx R7 <- [R2][R5]
loadimm R5 <- 2
aupd [R6][R5] <- R7
loadimm R5 <- 7
aidx R7 <- [R2][R5]
loadimm R5 <- 3
aupd [R6][R5] <- R7
loadimm R4 <- 9
cmovnz R2 <- R6 if R1 != 0
loadprog [0] <- [R0], PC=R4
aidx R6 <- [R2][R0]
loadimm R5 <- 4
aidx R7 <- [R2][R5]
loadimm R5 <- 5
aupd [R6][R5] <- R7
dealloc R2
cmovnz R2 <- R6 if R1 != 0
loadimm R5 <- 5
aidx R6 <- [R2][R5]
loadimm R7 <- 48
add R6 <- R6,R7
loadimm R5 <- 6
aupd [R2][R5] <- R6
loadimm R5 <- 6
aidx R6 <- [R2][R5]
out R6
loadimm R5 <- 4
aidx R6 <- [R2][R5]
loadimm R5 <- 3
aupd [R2][R5] <- R6
loadimm R5 <- 3
aidx R6 <- [R2][R5]
loadimm R4 <- 181
loadimm R5 <- 127
cmovnz R4 <- R5 if R6 != 0
loadprog [0] <- [R0], PC=R4
loadimm R6 <- 10
out R6
aidx R4 <- [R2][R1]
loadprog [0] <- [R0], PC=R4
loadimm R5 <- 8
aupd [R2][R5] <- R0
loadimm R5 <- 2
aidx R6 <- [R2][R5]
loadimm R5 <- 3
aupd [R2][R5] <- R6
loadimm R5 <- 3
aidx R6 <- [R2][R5]
loadimm R7 <- 10
div R6 <- R6,R7
loadimm R5 <- 4
aupd [R2][R5] <- R6
loadimm R5 <- 4
aidx R6 <- [R2][R5]
loadimm R7 <- 10
mul R6 <- R6,R7
loadimm R5 <- 7
aupd [R2][R5] <- R6
loadimm R5 <- 5
alloc [6][5], R6=6
aupd [R6][R0] <- R2
loadimm R7 <- 219
aupd [R6][R1] <- R7
loadimm R5 <- 3
aidx R7 <- [R2][R5]
loadimm R5 <- 2
aupd [R6][R5] <- R7
loadimm R5 <- 7
aidx R7 <- [R2][R5]
loadimm R5 <- 3
aupd [R6][R5] <- R7
loadimm R4 <- 9
cmovnz R2 <- R6 if R1 != 0
loadprog [0] <- [R0], PC=R4
aidx R6 <- [R2][R0]
loadimm R5 <- 4
aidx R7 <- [R2][R5]
loadimm R5 <- 5
aupd [R6][R5] <- R7
dealloc R2
cmovnz R2 <- R6 if R1 != 0
loadimm R5 <- 5
aidx R6 <- [R2][R5]
loadimm R7 <- 48
add R6 <- R6,R7
loadimm R5 <- 6
aupd [R2][R5] <- R6
loadimm R6 <- 2
alloc [7][6], R6=7
loadimm R5 <- 9
aupd [R2][R5] <- R6
loadimm R5 <- 6
aidx R6 <- [R2][R5]
loadimm R5 <- 9
aidx R7 <- [R2][R5]
aupd [R7][R0] <- R6
loadimm R5 <- 8
aidx R6 <- [R2][R5]
loadimm R5 <- 9
aidx R7 <- [R2][R5]
aupd [R7][R1] <- R6
loadimm R5 <- 9
aidx R6 <- [R2][R5]
loadimm R5 <- 8
aupd [R2][R5] <- R6
loadimm R5 <- 4
aidx R6 <- [R2][R5]
loadimm R5 <- 3
aupd [R2][R5] <- R6
loadimm R5 <- 3
aidx R6 <- [R2][R5]
loadimm R4 <- 260
loadimm R5 <- 191
cmovnz R4 <- R5 if R6 != 0
loadprog [0] <- [R0], PC=R4
loadimm R5 <- 8
aidx R6 <- [R2][R5]
loadimm R4 <- 288
loadimm R5 <- 266
cmovnz R4 <- R5 if R6 != 0
loadprog [0] <- [R0], PC=R4
loadimm R5 <- 8
aidx R6 <- [R2][R5]
aidx R6 <- [R6][R0]
loadimm R5 <- 6
aupd [R2][R5] <- R6
loadimm R5 <- 6
aidx R6 <- [R2][R5]
out R6
loadimm R5 <- 8
aidx R6 <- [R2][R5]
aidx R6 <- [R6][R1]
loadimm R5 <- 9
aupd [R2][R5] <- R6
loadimm R5 <- 8
aidx R6 <- [R2][R5]
dealloc R6
loadimm R5 <- 9
aidx R6 <- [R2][R5]
loadimm R5 <- 8
aupd [R2][R5] <- R6
loadimm R4 <- 260
loadprog [0] <- [R0], PC=R4
loadimm R6 <- 10
out R6
aidx R4 <- [R2][R1]
loadprog [0] <- [R0], PC=R4
loadimm R5 <- 8
alloc [8][5], R6=8
aupd [R6][R0] <- R2
loadimm R7 <- 300
aupd [R6][R1] <- R7
loadimm R4 <- 47
cmovnz R2 <- R6 if R1 != 0
loadprog [0] <- [R0], PC=R4
aidx R6 <- [R2][R0]
loadimm R5 <- 2
aidx R7 <- [R2][R5]
loadimm R5 <- 2
aupd [R6][R5] <- R7
dealloc R2
cmovnz R2 <- R6 if R1 != 0
loadimm R5 <- 2
aidx R6 <- [R2][R5]
mul R6 <- R6,R6
loadimm R5 <- 3
aupd [R2][R5] <- R6
loadimm R5 <- 10
alloc [9][5], R6=9
aupd [R6][R0] <- R2
loadimm R7 <- 324
aupd [R6][R1] <- R7
loadimm R5 <- 3
aidx R7 <- [R2][R5]
loadimm R5 <- 2
aupd [R6][R5] <- R7
loadimm R4 <- 185
cmovnz R2 <- R6 if R1 != 0
loadprog [0] <- [R0], PC=R4
aidx R6 <- [R2][R0]
dealloc R2
cmovnz R2 <- R6 if R1 != 0
aidx R4 <- [R2][R1]
loadprog [0] <- [R0], PC=R4
```

# Running the Emulator
The emulator takes a single filepath as input. The file must have a `.um` extension. For example, to do a timed run of sandmark, the command in linux would look like
`time ./um sandmark.um`

# Sandmark b146-46 Runtime

*Full Execution traces can be found in Emulator Execution Traces*

## -O2 Optimized
```
nrowe1@b146-46:~/cs554/cs554_um_nrowe1$ time ./um sandmark.um
...
...
real    0m12.708s
user    0m12.042s
sys     0m0.664s
```
## Unoptimized
```
nrowe1@b146-46:~/cs554/cs554_um_nrowe1$ time ./um sandmark.um
...
...
real    0m32.837s
user    0m32.153s
sys     0m0.681s
```

# Emulator Execution Traces
### helloworld.um
```
nrowe1@b146-46:~/cs554/cs554_um_nrowe1$ ./um helloworld.um
Hello world!
```
### square.um
```
nrowe1@b146-46:~/cs554/cs554_um_nrowe1$ ./um square.um
2
4

nrowe1@b146-46:~/cs554/cs554_um_nrowe1$ ./um square.um
350
122500

nrowe1@b146-46:~/cs554/cs554_um_nrowe1$ ./um square.um
2.2
33124
```
*The emulator has issues when passing decimal values to square.um*
### smlffact.um
```
nrowe1@b146-46:~/cs554/cs554_um_nrowe1_1$ ./um smlffact.um
12
479001600
```

# sandmark.um
```
nrowe1@b146-46:~/cs554/cs554_um_nrowe1_1$ date
Sun Sep  7 11:11:16 PM MDT 2025
nrowe1@b146-46:~/cs554/cs554_um_nrowe1_1$ time ./um sandmark.um
trying to Allocate array of size 0..
trying to Abandon size 0 allocation..
trying to Allocate size 11..
trying Array Index on allocated array..
trying Amendment of allocated array..
checking Amendment of allocated array..
trying Alloc(a,a) and amending it..
comparing multiple allocations..
pointer arithmetic..
check old allocation..
simple tests ok!
about to load program from some allocated array..
success.
verifying that the array and its copy are the same...
success.
testing aliasing..
success.
free after loadprog..
success.
loadprog ok.
 == SANDmark 19106 beginning stress test / benchmark.. ==
100. 12345678.09abcdef
99.  6d58165c.2948d58d
98.  0f63b9ed.1d9c4076
97.  8dba0fc0.64af8685
96.  583e02ae.490775c0
95.  0353a77b.2f02685c
94.  aa25a8d7.51cb07e5
93.  e13149f5.53a9ae5d
92.  abbbd460.86cf279c
91.  2c25e8d8.a71883a9
90.  dccf7b71.475e0715
89.  49b398a7.f293a13d
88.  9116f443.2d29be37
87.  5c79ba31.71e7e592
86.  19537c73.0797380a
85.  f46a7339.fe37b85a
84.  99c71532.729e2864
83.  f3455289.b84ced3d
82.  c90c81a9.b66fcd61
81.  087e9eef.fc1c13a6
80.  e933e2f5.3567082f
79.  25af849e.16290d7b
78.  57af9504.c76e7ded
77.  68cf6c69.6055d00c
76.  8e920fbd.02369722
75.  eb06e2de.03c46fda
74.  f9c40240.f1290b2a
73.  7f484f97.bc15610b
72.  1dabb00e.61e7b75b
71.  dceb40f5.207a75ca
70.  c3ed44f5.db631e81
69.  b7addb67.90460bf5
68.  ae710a90.04b433ef
67.  9ca2d5f0.05d3b631
66.  4f38abe0.4287cc05
65.  10d8691d.a5c934f8
64.  27c68255.52881eaa
63.  a0695283.110266b7
62.  336aa5dd.57287a9b
61.  b04fe494.d741ddbd
60.  2baf3654.9e33305a
59.  fd82095d.683efb19
58.  d0bac37f.badff9d7
57.  3be33fcc.d76b127e
56.  7f964f18.8b118ee1
55.  37aeddc8.26a8f840
54.  d71d55ff.6994c78f
53.  bf175396.f960cc54
52.  f6c9d8e1.44b81fd5
51.  6a9b4d86.fe7c66cb
50.  06bceb64.d5106aad
49.  237183b6.49c15b01
48.  4ec10756.6936136f
47.  9d1855a7.1e929fe8
46.  a641ede3.36bff422
45.  7bbf5ad4.dd129538
44.  732b385e.39fadce7
43.  b7f50285.e7f54c39
42.  42e3754c.da741dc1
41.  5dc42265.928ea0bb
40.  623fb352.3f25bc5b
39.  491f33d9.409bca87
38.  f0943bc7.89f512be
37.  80cdbc9d.8ad93517
36.  c1a8da99.32d37f3f
35.  91a0b15c.6df2cf4e
34.  50cf7a7a.f0466dc8
33.  02df4c13.14eb615d
32.  2963bf25.d9f06dfe
31.  c493d2db.f39ce804
30.  3b6e5a8e.5cf63bd7
29.  4c5c2fbe.8d881c00
28.  9b7354a6.81181438
27.  ae0fe8c6.ec436274
26.  e786b98d.f5a4111d
25.  a7719df1.d989d0b6
24.  beb9ebc0.6c56750d
23.  edf41fcb.e4cba003
22.  97268c46.713025f1
21.  deb087db.1349eb6a
20.  fc5221f0.3b4241bf
19.  3fa4370d.8fa16752
18.  044af7de.87b44b11
17.  2e86e437.c4cdbc54
16.  fd7cd8aa.63b6ca23
15.  631ceaad.e093a9d5
14.  01ca9732.52962532
13.  86d8bcf5.45bdf474
12.  8d07855b.0224e80f
11.  0f9d2bee.94d86c38
10.  5e6a685d.26597494
9.   24825ea1.72008775
8.   73f9c0b5.1480e7a3
7.   a30735ec.a49b5dad
6.   a7b6666b.509e5338
5.   d0e8236e.8b0e9826
4.   4d20f3ac.a25d05a8
3.   7c7394b2.476c1ee5
2.   f3a52453.19cc755d
1.   2c80b43d.5646302f
0.   a8d1619e.5540e6cf
SANDmark complete.

real    0m12.708s
user    0m12.042s
sys     0m0.664s
```
