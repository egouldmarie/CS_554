#include "instruction.hpp"
#include <cstdio>

Instruction::Instruction(uint32_t word) {
    // Extract opcode (bits 28-31)
    opcode = static_cast<Opcode>((word >> 28) & 0xF);
    
    if (opcode == Opcode::LOAD_IMMEDIATE) {
        // Special format for LOAD_IMMEDIATE
        regA = (word >> 25) & 0x7;  // bits 25-27
        immediate = word & 0x1FFFFFF;  // bits 0-24
        regB = regC = 0;  // unused
    } else {
        // Standard format
        regA = (word >> 6) & 0x7;   // bits 6-8
        regB = (word >> 3) & 0x7;   // bits 3-5
        regC = word & 0x7;          // bits 0-2
        immediate = 0;  // unused
    }
    
    // Debug output disabled for clarity
}
