#pragma once

#include <cstdint>

// Instruction opcodes
enum class Opcode : uint8_t {
    CONDITIONAL_MOVE = 0,
    ARRAY_INDEX = 1,
    ARRAY_UPDATE = 2,
    ADDITION = 3,
    MULTIPLICATION = 4,
    DIVISION = 5,
    NAND = 6,
    HALT = 7,
    ALLOCATION = 8,
    DEALLOCATION = 9,
    OUTPUT = 10,
    INPUT = 11,
    LOAD_PROGRAM = 12,
    LOAD_IMMEDIATE = 13
};

class Instruction {
public:
    // Decode a 32-bit instruction
    explicit Instruction(uint32_t word);
    
    // Get opcode
    Opcode getOpcode() const { return opcode; }
    
    // Get registers
    uint8_t getRegA() const { return regA; }
    uint8_t getRegB() const { return regB; }
    uint8_t getRegC() const { return regC; }
    
    // Get immediate value (for LOAD_IMMEDIATE)
    uint32_t getImmediate() const { return immediate; }

private:
    Opcode opcode;
    uint8_t regA;
    uint8_t regB;
    uint8_t regC;
    uint32_t immediate;  // Used only for LOAD_IMMEDIATE
};

