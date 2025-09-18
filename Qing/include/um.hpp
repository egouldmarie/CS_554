#pragma once

#include <cstdint>
#include <array>
#include "memory.hpp"
#include "instruction.hpp"

#include <array>
#include <cstdint>
#include <stdexcept>
#include <cstdlib>
#include <cstdio>

class UniversalMachine {
    friend class MemoryManager;  // Allow MemoryManager to access private members
public:
    UniversalMachine();
    ~UniversalMachine();

    // Load program from file
    void loadProgram(const char* filename);
    
    // Execute the loaded program
    void run();

protected:
    // 8 general purpose registers
    alignas(64) std::array<uint32_t, 8> registers;  // Aligned to cache line
    
    // Program counter
    uint32_t programCounter;
    
    // Memory manager
    MemoryManager memory;
    
    // Execute a single instruction
    inline void executeInstruction(const Instruction& inst) {
        switch (inst.getOpcode()) {
            case Opcode::CONDITIONAL_MOVE:
                if (registers[inst.getRegC()] != 0) {
                    registers[inst.getRegA()] = registers[inst.getRegB()];
                }
                break;
                
            case Opcode::ARRAY_INDEX:
                registers[inst.getRegA()] = memory.getValue(registers[inst.getRegB()], registers[inst.getRegC()]);
                break;
                
            case Opcode::ARRAY_UPDATE:
                memory.setValue(registers[inst.getRegA()], registers[inst.getRegB()], registers[inst.getRegC()]);
                break;
                
            case Opcode::ADDITION:
                registers[inst.getRegA()] = registers[inst.getRegB()] + registers[inst.getRegC()];
                break;
                
            case Opcode::MULTIPLICATION:
                registers[inst.getRegA()] = registers[inst.getRegB()] * registers[inst.getRegC()];
                break;
                
            case Opcode::DIVISION:
                if (registers[inst.getRegC()] == 0) {
                    throw std::runtime_error("Division by zero");
                }
                registers[inst.getRegA()] = registers[inst.getRegB()] / registers[inst.getRegC()];
                break;
                
            case Opcode::NAND:
                registers[inst.getRegA()] = ~(registers[inst.getRegB()] & registers[inst.getRegC()]);
                break;
                
            case Opcode::HALT:
                exit(0);
                break;
                
            case Opcode::ALLOCATION:
                registers[inst.getRegB()] = memory.allocate(registers[inst.getRegC()]);
                break;
                
            case Opcode::DEALLOCATION:
                memory.deallocate(registers[inst.getRegC()]);
                break;
                
            case Opcode::OUTPUT:
                if (registers[inst.getRegC()] > 255) {
                    throw std::runtime_error("Invalid output value");
                }
                putchar(registers[inst.getRegC()]);
                break;
                
            case Opcode::INPUT: {
                int c = getchar();
                registers[inst.getRegC()] = (c == EOF) ? ~0u : (static_cast<uint32_t>(c) & 0xFF);
                break;
            }
                
            case Opcode::LOAD_PROGRAM: {
                uint32_t arrayId = registers[inst.getRegB()];
                memory.duplicateArray(arrayId);
                programCounter = registers[inst.getRegC()];
                return;  // Skip incrementing program counter
            }
                
            case Opcode::LOAD_IMMEDIATE:
                registers[inst.getRegA()] = inst.getImmediate();
                break;
        }
        ++programCounter;
    }
    
    // Helper function to check if a value is within valid output range (0-255)
    inline bool isValidOutput(uint32_t value) const { return value <= 255; }
};
