#include "memory.hpp"
#include <stdexcept>

MemoryManager::MemoryManager() : nextId(1), poolOffset(0) {
    // Pre-allocate memory pool
    memoryPool.reserve(MEMORY_POOL_SIZE);
    
    // Pre-allocate array map
    arrays.reserve(INITIAL_ARRAYS);
    
    // Initialize array 0 (program array)
    arrays[0] = std::vector<uint32_t>();
    arrays[0].reserve(MEMORY_POOL_SIZE / 16);  // Reasonable size for program
}

MemoryManager::~MemoryManager() = default;

uint32_t MemoryManager::allocate(uint32_t size) {
    uint32_t id;
    if (!freeIds.empty()) {
        id = freeIds.front();
        freeIds.pop_front();
    } else {
        id = nextId++;
    }
    
    auto& array = arrays[id];
    array.reserve(size);
    array.resize(size, 0);
    return id;
}

void MemoryManager::deallocate(uint32_t id) {
    if (id == 0) {
        throw std::runtime_error("Cannot deallocate program array (id 0)");
    }
    
    auto it = arrays.find(id);
    if (it == arrays.end()) {
        throw std::runtime_error("Attempt to deallocate inactive array");
    }
    
    arrays.erase(it);
    freeIds.push_back(id);
}

void MemoryManager::loadProgram(const std::vector<uint32_t>& program) {
    auto& array = arrays[0];
    array.reserve(program.size());
    array = program;
}

void MemoryManager::duplicateArray(uint32_t sourceId) {
    auto it = arrays.find(sourceId);
    if (it == arrays.end()) {
        throw std::runtime_error("Attempt to load program from inactive array");
    }
    
    auto& array = arrays[0];
    array.reserve(it->second.size());
    array = it->second;
}

