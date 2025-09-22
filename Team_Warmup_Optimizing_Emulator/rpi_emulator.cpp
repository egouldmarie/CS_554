#include <iostream>
#include <fstream>
#include <bitset>
#include <vector>
#include <map>
#include <cstdint>
#include <string>
#include <cstdlib>
#include <cstring>


using namespace std;

typedef uint32_t word;
const int wordSize = sizeof(word);

/* OpCode enumeration */
typedef enum {
    COND_MOVE,   //  0
    ARR_INDEX,   //  1
    ARR_UPDATE,  //  2
    ADD,         //  3
    MULT,        //  4
    DIV,         //  5
    NAND,        //  6
    HALT,        //  7
    ALLOC,       //  8
    DEALLOC,     //  9
    OUTPUT,      // 10
    INPUT,       // 11
    LOAD_PROG,   // 12
    LOAD_IMMED,  // 13
} OpCode;

// A 5-int array to hold the OpCode, A, B, C, value
// for a parsed instruction.
uint32_t decoded_instruction[5];

/**
 * @brief Parse a 32-bit instruction into components.
 * @param inst A 32-bit instruction word.
 * @return void. Stores result in global 'decoded_instruction' array.
*/
void decode_instruction(const uint32_t inst) {

    uint32_t opcode = 0, a = 0, b = 0, c = 0, value = 0;

    opcode = inst >> 28;

    if (opcode < LOAD_IMMED) {

        a = (inst >> 6) & 0x7;
        b = (inst >> 3) & 0x7;
        c = inst        & 0x7;

    } else if (opcode == LOAD_IMMED) {

        a  = (inst >> 25) & 0x7; 
        value = inst & ((1 << 25) - 1);

    } else {

        // not a valid opcode, so interpret
        // entire 32-bit instruction as a value
        value = inst;
    }

    decoded_instruction[0] = opcode;
    decoded_instruction[1] = a;
    decoded_instruction[2] = b;
    decoded_instruction[3] = c;
    decoded_instruction[4] = value;
}

int main(int argc, char *argv[])
{
    // initialize machine
    word registers[8] = {0};
    map<word, vector<word>> arrays = {};
    vector<word> freeIdentifiers = {};

    // load program
    if (argc > 1)
    {
        // open the file:
        basic_ifstream<char> filestream(argv[1], ios::binary);

        if (!filestream)
        {
            printf("File not found.\n");
            exit(-1);
        }

        filestream.seekg(0, ios::end);
        size_t fileSize = filestream.tellg() / 4;
        filestream.seekg(0, ios::beg);

        word tempWord;
        for (auto i = 0; i < fileSize; ++i)
        {
            filestream.read(reinterpret_cast<char *>(&tempWord), wordSize);
            arrays[0].push_back(((0xFF000000 & tempWord) >> 24) |
                                ((0x00FF0000 & tempWord) >> 8) |
                                ((0x0000FF00 & tempWord) << 8) |
                                ((0x000000FF & tempWord) << 24));
        }
        filestream.close();

        uint32_t opcode_alt = 0, a = 0, b = 0, c = 0, value = 0;

        // run
        for (uint32_t it = 0; it < arrays[0].size(); ++it)
        {
            word instruction = arrays[0][it];
            decode_instruction(instruction);
            opcode_alt = decoded_instruction[0];
            a = decoded_instruction[1];
            b = decoded_instruction[2];
            c = decoded_instruction[3];
            value = decoded_instruction[4];

            // BEGIN ALTERNATE
            if (opcode_alt == 0)
            {
                // The register A receives the value in register B, unless the register C contains 0.
                if (registers[c] != 0)
                {
                    registers[a] = registers[b];
                }
            }
            else if (opcode_alt == 1)
            {
                // The register A receives the value stored at offset in register C in the array identified by B.
                registers[a] = arrays[registers[b]][registers[c]];
            }
            else if (opcode_alt == 2)
            {
                // The array identified by A is updated at the offset in register B to store the value in register C.
                arrays[registers[a]][registers[b]] = registers[c];
            }
            else if (opcode_alt == 3)
            {
                // The register A receives the value in register B plus the value in register C, modulo 2^32.
                registers[a] = registers[b] + registers[c];
            }
            else if (opcode_alt == 4)
            {
                // The register A receives the value in register B times the value in register C, modulo 2^32
                registers[a] = registers[b] * registers[c];
            }
            else if (opcode_alt == 5)
            {
                // The register A receives the value in register B divided by the value in register C, if any,
                // where each quantity is treated as an unsigned 32-bit number.

                // If the program attempts to divide by 0, then the machine will Fail.
                if (registers[c] == 0)
                {
                    printf("Attempted to divide by zero.\n");
                    exit(-1);
                }

                registers[a] = registers[b] / registers[c];
            }
            else if (opcode_alt == 6)
            {
                // Each bit in the register A receives the 1 bit if either register B or register C has a 0 bit in that position.
                // Otherwise the bit in register A receives the 0 bit.
                registers[a] = ~(registers[b] & registers[c]);
            }
            else if (opcode_alt == 7)
            {
                // The machine stops computation.
                printf("Halt.\n");
                exit(0);
            }
            else if (opcode_alt == 8)
            {
                // A new array is created; the value in the register C gives the number of words in the new array. This new array is
                // zero-initialized. A bit pattern not consisting of exclusively the 0 bit, and that identifies no other active allocated array,
                // is placed in the B register, and it identifies the new array.
                if (arrays.size() < 0xFFFFFFFF)
                {
                    word idx;
                    if (freeIdentifiers.size() > 0)
                    {
                        idx = freeIdentifiers.back();
                        freeIdentifiers.pop_back();
                    }
                    else
                    {
                        for (word id = arrays.size(); id < 0xFFFFFFFF; ++id)
                        {
                            if (arrays.count(id) == 0)
                            {
                                idx = id;
                                break;
                            }
                        }
                    }

                    arrays[idx] = vector<word>(registers[c], 0);
                    registers[b] = idx;
                }
                else
                {
                    printf("Ran out of arrays to allocate.\n");
                    exit(-1);
                }
            }
            else if (opcode_alt == 9)
            {
                // The array identified by the register C is deallocated (freed).
                // Future allocations may then reuse that identifier.
                if (registers[c] == 0)
                {
                    // If the program attempts to deallocate the ’0’ array, or to
                    // deallocate an array that is not active, then the machine will Fail.
                    printf("Attempted to deallocate the '0' array.\n");
                    exit(-1);
                }
                else if (arrays.count(registers[c]) == 0)
                {
                    printf("Attempted to deallocate unallocated array.\n");
                    exit(-1);
                }

                arrays.erase(registers[c]);
                freeIdentifiers.push_back(registers[c]);
            }
            else if (opcode_alt == 10)
            {
                //  The value in the register C is displayed on the console. Only values in the range 0–255 are allowed.
                if (registers[c] > 255)
                {
                    printf("Output was larger than 255.\n");
                    exit(-1);
                }
                cout << (char)registers[c];
            }
            else if (opcode_alt == 11)
            {
                // The machine waits for input on the console. When input arrives, the register C is loaded with the input, which
                // must be in the range 0–255. If the end of input has been signaled, then the register C is filled with all 1’s.
                if (cin.eof())
                {
                    registers[c] = 0xFFFFFFFF;
                }
                else
                {
                    char input;
                    cin.get(input);
                    registers[c] = (word)input;
                }
            }
            else if (opcode_alt == 12)
            {
                // The array identified by the B register is duplicated and the duplicate replaces the ‘0’ array, regardless of size.
                // The program counter is updated to indicate the word of this array that is described by the offset given in C, where the
                // value 0 denotes the first word, 1 the second, etc.

                if (registers[b] != 0)
                {
                    arrays[0] = arrays[registers[b]];
                }

                it = registers[c] - 1;
            }
            else if (opcode_alt == 13)
            {
                // The value in bits 0:24 is loaded into the register A (given by bits 25:27).
                registers[a] = arrays[0][it] & 0x1FFFFFF;
            }
            else
            {
                // unrecognized opcode
                printf("Unrecognized opcode.\n");
                exit(-1);
            }
            // END ALTERNATE
        }

        return 0;
    }
    else
    {
        return -1;
    }
}