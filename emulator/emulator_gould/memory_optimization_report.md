# Memory Optimization Report 

## Overview
This report describes three memory optimization approaches implemented for the Universal Machine emulator.  

I only listed a few relatively complete attempts. These attempts actually did not achieve good performance in this Simulator, possibly because array operations are not frequent enough small block allocations/releases, and each allocation requires traversing the linked list to find a suitable block, or due to other reasons. In my initial Simulator, there was roughly a 10-second improvement. But I included them here just to provide some possible solution ideas, though it seems deeper thought is needed.

## 1. Memory Pool Optimization
I apple "efficient" management of small arrays (≤1024 words) and it can reduce allocation/deallocation overhead in theory.

### Implementation
```cpp
class MemoryPool {
    static constexpr size_t BLOCK_SIZE = 1024;
    vector<vector<word>> blocks;
    vector<size_t> freeBlocks;
}
```
## 2. Dynamic Memory Allocation
It is used to custom memory management for better control and direct block management

### Implementation
```cpp
class DynamicAllocator {
    list<MemoryBlock*> blocks;
    static constexpr size_t MIN_BLOCK_SIZE = 64;
    static constexpr size_t MAX_BLOCKS = 1024;
}
```
## 3. Memory Pre-allocation
It is used to reduce runtime allocation overhead and prevent memory fragmentation

### Implementation
```cpp
constexpr size_t INITIAL_ARRAY_SIZE = 1024 * 1024;  // 1M words
constexpr size_t INITIAL_FREE_IDS = 1024;
arrays[0].reserve(INITIAL_ARRAY_SIZE);
freeIdentifiers.reserve(INITIAL_FREE_IDS);
```
