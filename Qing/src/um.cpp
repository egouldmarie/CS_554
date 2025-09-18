#include "um.hpp"
#include <fstream>
#include <vector>

UniversalMachine::UniversalMachine() : programCounter(0) {
    registers.fill(0);
}

UniversalMachine::~UniversalMachine() = default;

void UniversalMachine::loadProgram(const char* filename) {
    std::ifstream file(filename, std::ios::binary);
    if (!file) {
        throw std::runtime_error("Could not open program file");
    }
    
    file.seekg(0, std::ios::end);
    size_t fileSize = file.tellg();
    file.seekg(0, std::ios::beg);
    
    if (fileSize % 4 != 0) {
        throw std::runtime_error("Invalid program file size");
    }
    
    std::vector<uint32_t> program(fileSize / 4);
    std::vector<char> buffer(fileSize);
    
    file.read(buffer.data(), fileSize);
    
    for (size_t i = 0; i < fileSize; i += 4) {
        uint32_t word = (static_cast<uint32_t>(static_cast<unsigned char>(buffer[i])) << 24) |
                       (static_cast<uint32_t>(static_cast<unsigned char>(buffer[i + 1])) << 16) |
                       (static_cast<uint32_t>(static_cast<unsigned char>(buffer[i + 2])) << 8) |
                       static_cast<uint32_t>(static_cast<unsigned char>(buffer[i + 3]));
        program[i / 4] = word;
    }
    
    memory.loadProgram(program);
}

void UniversalMachine::run() {
    const auto& program = memory.arrays.at(0);
    
    while (true) {

        executeInstruction(Instruction(program[programCounter]));
    }
}