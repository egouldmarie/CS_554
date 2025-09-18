#pragma once

#include <cstddef>
#include <cstdint>
#include <vector>
#include <unordered_map>
#include <queue>
#include <deque>

class UniversalMachine;  

class MemoryManager {
    friend class UniversalMachine;  
public:
    static constexpr std::size_t INITIAL_ARRAYS = 1024;
    static constexpr std::size_t MEMORY_POOL_SIZE = 1024 * 1024;  

    MemoryManager();
    ~MemoryManager();

    uint32_t allocate(uint32_t size);
    
    void deallocate(uint32_t id);
    
    inline uint32_t getValue(uint32_t arrayId, uint32_t offset) const {
        const auto& array = arrays.at(arrayId);
        return offset < array.size() ? array[offset] : 0;
    }
    
    inline void setValue(uint32_t arrayId, uint32_t offset, uint32_t value) {
        auto& array = arrays.at(arrayId);
        if (offset < array.size()) {
            array[offset] = value;
        }
    }
    void loadProgram(const std::vector<uint32_t>& program);
    
    void duplicateArray(uint32_t sourceId);

private:

    std::unordered_map<uint32_t, std::vector<uint32_t>> arrays;

    std::deque<uint32_t> freeIds;
    

    std::vector<uint32_t> memoryPool;
    std::size_t poolOffset;
    
    uint32_t nextId;
};

