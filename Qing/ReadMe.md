# Exercise 2 qinghong shao
In this part, I didn't finish my 2nd assignment successfully, there are some errors left. I will try again and submit it at exercise 3. However, I finish my first exercise, a simulator.

## Report:
```bash
qinghongshao@b146-46:~/exercise2qinghong/build$ date
Thu Aug 28 02:50:46 PM MDT 2025
qinghongshao@b146-46:~/exercise2qinghong/build$ time ./um ../sandmark.um
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

real    0m44.078s
user    0m44.065s
sys     0m0.008s
qinghongshao@b146-46:~/exercise2qinghong/build$
```

## Acknowledgment
In completing Exercise 2, I made use of advanced AI tools, specifically GPT-5 and Claude 3.5. Both are paid services (though students can currently access them for free). 
I primarily relied on these tools for: 
- Constructing the overall code framework for the emulator project. 
- Optimizing the performance of the simulator, particularly from the perspective of memory usage and efficiency. 

### Prompts Used
1. “Please read the assignment requirements I provided, and give me step-by-step instructions on how to construct the entire project. Also, suggest an appropriate framework for the project, including the testing section.” 
2. “Please give me suggestions for performance optimization, especially from the perspective of memory usage.” 

### AI Responses
1.
```
project/
 ├── src/
 │   ├── emulator/
 │   │   ├── mod.rs          # Emulator module
 │   │   └── memory.rs       # Memory management implementation
 │   ├── assembler/
 │   │   ├── mod.rs          # Assembler module
 │   │   └── parser.rs       # Assembly language parser
 │   ├── disassembler/
 │   │   └── mod.rs          # Disassembler module
 │   └── main.rs             # Program entry
 ├── tests/
 │   ├── test_emulator.rs
 │   ├── test_assembler.rs
 │   └── test_disassembler.rs
 ├── examples/
 │   ├── helloworld.uma
 │   ├── square.uma
 │   └── sandmark.uma
 ├── Cargo.toml              # Project dependencies
 └── README.md               # Project documentation
```

### Technology Choice
According to the assignment requirements, we can choose between C, C++, or Rust. I recommend using Rust for the following reasons:
1. Memory safety guarantees
2. Strong type system and pattern matching
3. Excellent performance characteristics
4. Built-in testing framework
5. Superior package management system

**Implementation Steps**

**Emulator Implementation**

1. Implement basic memory management system

- Array allocation and management
- Memory segment creation and recycling

1. Implement instruction decoder

- Parse 32-bit instructions
- Identify opcodes and operands

1. Implement instruction execution unit

- Implement all instruction operations
- Handle program counter

1. Implement I/O operations

- Standard input/output handling
- Error handling mechanism

**3.2 Disassembler Implementation**

1. Implement binary file reading
2. Implement instruction parsing

- Convert binary instructions to readable assembly format
- Add useful comments and labels

1. Implement formatted output

- Clear instruction display
- Address and opcode display

**3.3 Assembler Implementation**

1. Implement assembly language parser

- Lexical analysis
- Syntax analysis

1. Implement symbol table management

- Label handling
- Address resolution

1. Implement code generation

- Generate binary instructions
- Handle address relocation

**4. Testing Framework**

1. Unit tests

- Basic functionality tests for each module
- Boundary condition tests

1. Integration tests

- Complete program execution tests
- Example program tests (helloworld.uma, square.uma, etc.)

1. Performance tests

- Sandmark benchmark
- Performance analysis and optimization

**5. Documentation**

1. Code documentation

- Detailed comments for functions and modules
- API documentation

1. README documentation

- Project overview
- Build and run instructions
- Test results report
- AI tool usage documentation (if used)

2.

**1. Memory Management Optimization**

**1.1 Memory Pool Strategy**

- Implement a custom memory pool for frequent allocations
- Use fixed-size block allocation for common memory sizes
- Consider using memory arena for temporary allocations
- Implement object pooling for frequently created/destroyed     objects

**1.2 Cache Optimization**

- Design cache-friendly data structures
- Implement an LRU (Least Recently Used) cache for frequently     accessed memory segments
- Use cache prefetching for predictable memory access patterns
- Consider implementing a two-level cache system (L1/L2) for     different access patterns

**1.3 Memory Layout Optimization**

- Organize data structures to minimize cache misses
- Separate hot (frequently accessed) and cold (rarely accessed)     data
- Use data alignment to optimize memory access
- Consider Structure of Arrays (SoA) vs Array of Structures (AoS)     based on access patterns

**2. Instruction Execution Optimization**

**2.1 Instruction Processing**

- Implement instruction caching for frequently executed code     paths
- Use jump tables for efficient instruction dispatch
- Consider implementing a simple instruction pipeline
- Optimize branch prediction through careful code organization

**2.2 Register Management**

- Implement efficient register allocation strategies
- Minimize register spilling through careful allocation
- Track register usage patterns for optimization
- Consider using register renaming for parallel execution

**3. Algorithm and Data Structure Optimization**

**3.1 Data Structure Selection**

- Choose appropriate containers from STL based on usage patterns
- Consider custom containers for specific use cases
- Use flat data structures where possible to improve cache     locality
- Implement specialized containers for frequently used operations

**3.2 Algorithm Optimization**

- Use efficient sorting and searching algorithms
- Implement lazy evaluation where appropriate
- Consider using bit manipulation for optimization
- Optimize critical paths based on profiling results

**4. C++ Specific Optimizations**

**4.1 Modern C++ Features**

- Use move semantics to reduce copying
- Implement perfect forwarding where appropriate
- Use constexpr for compile-time computation
- Leverage template metaprogramming for zero-cost abstractions

**4.2 Compiler Optimizations**

- Use appropriate compiler flags (-O2, -O3)
- Consider profile-guided optimization (PGO)
- Use inline functions where beneficial
- Leverage SIMD instructions through compiler intrinsics

**5. Performance Monitoring**

**5.1 Profiling Strategy**

- Implement performance counters for key metrics
- Track memory usage and allocation patterns
- Monitor cache hit/miss rates
- Measure instruction execution times

**5.2 Analysis Tools**

- Use built-in profiling tools
- Implement custom performance metrics
- Track system resource usage
- Monitor memory leaks and fragmentation

**6. Best Practices for Implementation**

**6.1 General Guidelines**

- Start with clean, maintainable code
- Optimize only after profiling
- Document performance-critical sections
- Maintain balance between readability and performance

**6.2 Memory Access Patterns**

- Minimize cache line bouncing
- Reduce false sharing in multi-threaded code
- Use appropriate memory barriers
- Implement efficient memory prefetching

**7. Optimization Priorities**

1. First Priority

- Basic memory management optimization
- Critical path optimization
- Cache-friendly data structures
- Essential performance monitoring

1. Second Priority

- Advanced caching strategies
- Instruction optimization
- Complex data structure optimization
- Detailed profiling systems

1. Third Priority

- Fine-tuning optimizations
- Advanced compiler optimizations
- Specialized algorithms
- Extended monitoring capabilities

**8. Implementation Recommendations**

1. Initial Phase

- Implement basic functionality
- Set up performance monitoring
- Establish baseline measurements
- Identify critical paths

1. Optimization Phase

- Focus on high-impact areas first
- Implement memory optimizations
- Improve instruction processing
- Enhance data structures

1. Fine-tuning Phase

- Optimize based on profiling results
- Implement advanced features
- Fine-tune performance
- Document optimizations

**9. Testing and Validation**

1. Performance Testing

- Implement benchmark suite
- Test with various input sizes
- Measure resource usage
- Compare against baseline

1. Validation

- Verify correctness after optimization
- Test edge cases
- Ensure stability
- Document performance improvements

Remember to:

- Always measure before and after optimization
- Focus on bottlenecks identified through profiling
- Maintain code readability while optimizing
- Document performance-critical decisions
- Test thoroughly after each optimization
- Consider the trade-offs between performance and maintainability

These optimization strategies should be applied incrementally, always measuring the impact of each change to ensure it provides meaningful improvement without compromising code quality or maintainability.

**References**

https://github.com/gbroques/compiler

https://pku-minic.github.io/online-doc/

https://norasandler.com/2017/11/29/Write-a-Compiler.html

