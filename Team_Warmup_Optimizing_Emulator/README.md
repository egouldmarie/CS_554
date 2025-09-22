# Assignment: Team Warmup Exercise: Optimizing the Emulator

## Completed by the Raspberry Pi group:
**Authors: Emma Gould      (egould@unm.edu)**<br/>
         **Nathan J. Rowe  (nrowe1@unm.edu)**<br/>
         **Qinghong Shao   (qinghongshao@unm.edu)**<br/>
         **Warren D. Craft (wdcraft@unm.edu)**<br/>

## Assignment Description/Details from CANVAS Course Site

> Available until Sep 21 at 11:59pm Sep 21 at 11:59pm
> Due Sep 21 at 11:59pm Sep 21 at 11:59pm
> 
> Put together the best ideas from your team members' solutions,
> and brainstorm to further improve the um emulator from the homework
> exercises.
> 
> Make sure that your team's emulator is able to execute this program:
> umix.umDownload umix.um
> 
> Then, report the performance of the emulator for sandmark.
> 
> This time, in addition to timing on b146-46.cs.unm.edu, time it on
> risc-machine-2.cs.unm.edu as well.
> 
> Keep in mind, this submission will count for everyone in your Groups
> for the compiler project group.

## Overview

We were tempted to work on that emulator among us that was already the
fastest, but instead thought it would be a good exercise to focus on
one of our emulators (in C++) that was still not quite completing the
sandmark.um criterion. 

Debugging the emulator was challenging, because the problem was subtle
and easily missed, eventually turning out to involve a swapping of two
lines of code in the implementation of OpCode 8 (Allocation), that only
triggered an issue when B and C identified the same register. Once we
got that working and able to run sandmark, we had an initial execution
time on the b146-46.cs.unm.edu machine of roughly 3 mins, 30 secs. 

Initial timing investigations yielded the following data, which helped
focus our attention on both the most over-all time-consuming and the
most expensive in terms of average execution time. Additionally,
review of the code turned up a few promising targets for improvement;
the implementation of the memory utilized a map with O(logn) time for
sorting, the interpretations of the instructions included unnecessary
conditional if-else statements, and the use of vectors rather than
arrays resulting in expensive calls to .size() and .count() during
every program instruction interpretation. 

We improved these issues by replacing the map with an unordered map
for the memory, resulting in O(1) time since our allocation was in
order, removing unnecessary conditional statements, and keeping
variables outside of the program for() loop that stored the number
of arrays that had been allocated and the size of the current 0
array, eliminating all but one necessary vector .size() call.

Timing appearing below shows execution times for the various OpCodes
executed during the running of the sandmark.um program, along
with changes in times after optimization work (negative times indicate
improvements).

|opcode	| mean time (ns)	| # calls	|     (total secs) |  ∆ (secs) |  ∆ (%) |
|-------|-----------------------|---------------|------------------|-----------|--------|
|0	|    18.984	    |    356404848	|        6.77 | -1.09	|    16.0| 
|1	|    41.898	    |    979571632	|      41.04  | -22.12	| 53.9 |
|2	|    70.349	    |    747283504	|       52.57  | -38.29	| 72.8 |
|3	|    15.056	    |     92344429	 |       1.39  |  0.08	| 6.0|
|4	|    15.191	    |     40860531	 |       0.62  |  0.04	| 6.9 |
|5	|    19.871	    |      4987085	 |       0.10  | -0.02	| 19.2 |
|6	|    15.165	    |    389368029	 |       5.90  |  0.31	| 5.3 |
|8	|   189.758	    |     91964700	 |      17.45  | -12.70	| 72.8 |
|9	|   124.42	    |     91949290	 |      11.44  | -6.37	| 55.7 |
|10	|   293.399	    |         2946	 |       0.00  |  0.00    | 118.8| 
|12	|    38.122	    |    395373297	 |      15.07  | -8.78	| 58.2 |
|13	|    15.264	    |   2365891287	 |      36.11  |  1.69	| 4.7|

### Initital sandmark.um runtime (b146-46.cs.unm.edu)
```
real    3m29.994s
user    3m29.980s
sys     0m0.009s
```
### Final sandmark.um runtime (b145-46.cs.unm.edu)
```
real	0m40.217s 
user	0m40.206s 
sys	0m0.008s
```

EXAMPLE TRACES are shown further below for program file sandmark.um
run remotely on machines b146-46.cs.unm.edu and risc-machine-2.cs.unm.edu. 


## EXAMPLES
### sandmark.um on b146:

```
Output from b146-46: 

egould@b146-46:~$ g++ ./rpi_emulator.cpp -o emulator -O3 
egould@b146-46:~$ time ./emulator ./sandmark.um  
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
real	0m40.217s 
user	0m40.206s 
sys	0m0.008s 
```

### sandmark.um on risc-machine-2:

```
Output from risc-machine-2: 

egould@risc-machine-2:~$ g++ -o emulator rpi_emulator.cpp -O3 
egould@risc-machine-2:~$ time ./emulator ./sandmark.um 
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

real	4m14.870s 
user	4m14.749s 
sys	0m0.048s
```

### umix.um:

```
12:00:00 1/1/19100 

Welcome to Universal Machine IX (UMIX). 


This machine is a shared resource. Please do not log 

in to multiple simultaneous UMIX servers. No game playing 

is allowed. 


Please log in (use 'guest' for visitor access). 

;login: guest 

logged in as guest 

INTRO.LOG=200@3038|70f135d810a36771143150c56b999c5 


You have new mail. Type 'mail' to view. 

% mail 

First unread message: 

--------------------- 

Date: Fri, 1 Jan 19100 00:00:00 -0400 

From: Administrator <root@localhost> 

To: guest@cbv.net 

Subject: guest account misuse 

To whom it may concern: 

Guest access is provided as a courtesy to the community. We have 

recently observed an increase in abuse using the guest account. For 

example, the following sequence of commands obviously represents an 

attempt to gain unauthorized access to the account "howie": 

  cd code 

  /bin/umodem hack.bas STOP 

  /bin/qbasic hack.bas 

  ls /home 

  ./hack.exe howie 

Moreover, the file that you uploaded with umodem appears to be  

corrupted and did not compile. 

  

Please have respect for your fellow users, 

Admin 

% cd code 

% /bin/umodem hack.bas STOP 

umodem : file hack.bas already exists. 

% /bin/qbasic hack.bas 

V SKIP 

X SKIP 

XV SKIP 

XX SKIP 

XXV SKIP 

XXX SKIP 

XXXV SKIP 

XL SKIP 

XLV SKIP 

L SKIP 

LV SKIP 

LX SKIP 

LXV IF (ARGS() > I) THEN GOTO LXXXV ELSE SKIP 

LXX PRINT "usage: ./hack.exe username" 

LXXV PRINT CHR(X) 

LXXX END 

LXXXV SKIP 

XC SKIP 

XCV DIM username AS STRING 

C SET username = ARG(II) 

CV SKIP 

CX DIM pwdcount AS INTEGER 

CXV SET pwdcount = LIII 

CXX DIM words(pwdcount) AS STRING 

CXXV SET words(I) = "airplane" 

CXXX SET words(II) = "alphabet" 

CXXXV SET words(III) = "aviator" 

CXL SET words(IV) = "bidirectional" 

CXLV SET words(V) = "changeme" 

CL SET words(VI) = "creosote" 

CLV SET words(VII) = "cyclone" 

CLX SET words(VIII) = "december" 

CLXV SET words(IX) = "dolphin" 

CLXX SET words(X) = "elephant" 

CLXXV SET words(XI) = "ersatz" 

CLXXX SET words(XII) = "falderal" 

CLXXXV SET words(XIII) = "functional" 

CXC SET words(XIV) = "future" 

CXCV SET words(XV) = "guitar" 

CC SET words(XVI) = "gymnast" 

CCV SET words(XVII) = "hello" 

CCX SET words(XVIII) = "imbroglio" 

CCXV SET words(XIX) = "january" 

CCXX SET words(XX) = "joshua" 

CCXXV SET words(XXI) = "kernel" 

CCXXX SET words(XXII) = "kingfish" 

CCXXXV SET words(XXIII) = "(\b.bb)(\v.vv)" 

CCXL SET words(XXIV) = "millennium" 

CCXLV SET words(XXV) = "monday" 

CCL SET words(XXVI) = "nemesis" 

CCLV SET words(XXVII) = "oatmeal" 

CCLX SET words(XXVIII) = "october" 

CCLXV SET words(XXIX) = "paladin" 

CCLXX SET words(XXX) = "pass" 

CCLXXV SET words(XXXI) = "password" 

CCLXXX SET words(XXXII) = "penguin" 

CCLXXXV SET words(XXXIII) = "polynomial" 

CCXC SET words(XXXIV) = "popcorn" 

CCXCV SET words(XXXV) = "qwerty" 

CCC SET words(XXXVI) = "sailor" 

CCCV SET words(XXXVII) = "swordfish" 

CCCX SET words(XXXVIII) = "symmetry" 

CCCXV SET words(XXXIX) = "system" 

CCCXX SET words(XL) = "tattoo" 

CCCXXV SET words(XLI) = "thursday" 

CCCXXX SET words(XLII) = "tinman" 

CCCXXXV SET words(XLIII) = "topography" 

CCCXL SET words(XLIV) = "unicorn" 

CCCXLV SET words(XLV) = "vader" 

CCCL SET words(XLVI) = "vampire" 

CCCLV SET words(XLVII) = "viper" 

CCCLX SET words(XLVIII) = "warez" 

CCCLXV SET words(XLIX) = "xanadu" 

CCCLXX SET words(L) = "xyzzy" 

CCCLXXV SET words(LI) = "zephyr" 

CCCLXXX SET words(LII) = "zeppelin" 

CCCLXXXV SET words(LIII) = "zxcvbnm" 

CCCXC SKIP 

CCCXCV PRINT ((("attempting hack with " + pwdcount) + " passwords ") + CHR(X)) 

CD DIM i AS INTEGER 

CDV SET i = I 

CDX IF CHECKPASS(username, words(i)) THEN GOTO CDXXX ELSE SKIP 

CDXV SET i = (i + I) 

CDXX IF (i > pwdcount) THEN GOTO CDXLV ELSE SKIP 

CDXXV GOTO CDX 

CDXXX PRINT (("found match!! for user " + username) + CHR(X)) 

CDXXXV PRINT (("password: " + words(i)) + CHR(X)) 

CDXL END 

CDXLV PRINT (("no simple matches for user " + username) + CHR(X)) 

CDL SKIP 

CDLV SKIP 

CDLX SKIP 

CDLXV SKIP 

CDLXX SKIP 

CDLXXV SKIP 

CDLXXX SKIP 

CDLXXXV SKIP 

CDXC SET i = I 

CDXCV DIM j AS INTEGER 

qbasic: SYNTAX ERROR: EXPECTED  LINENVM STATEMENT 

% ls /home 

ftd/ 

guest/ 

gardener/ 

ohmega/ 

yang/ 

howie/ 

hmonk/ 

bbarker/ 

% ./hack.exe howie 

unknown command ./hack.exe 

new to UMIX? try 

  help 

for help. 

% help 

For information on a specific command, type 

  help cmd 

UMIX Commands: 

  ls 

  rm 

  cat 

  more 

  cdup 

  mkdir 

  cd 

  run 

  pwd 

  logout 

Also, try running programs with no arguments for usage instructions. 
% exit 
```
