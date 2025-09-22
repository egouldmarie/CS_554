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

        // run
        for (uint32_t it = 0; it < arrays[0].size(); ++it)
        {
            bitset<32> bits = arrays[0][it];

            // Standard instructions use three registers, A, B, and C. Each register is described by a three
            // bit segment of the instruction. Register A is given by bits 6:8, B is given by bits 3:5, and
            // C is given by bits 0:2.
            bitset<3> A;
            A[0] = bits[6];
            A[1] = bits[7];
            A[2] = bits[8];
            bitset<3> B;
            B[0] = bits[3];
            B[1] = bits[4];
            B[2] = bits[5];
            bitset<3> C;
            C[0] = bits[0];
            C[1] = bits[1];
            C[2] = bits[2];

            // The operation code is given by bits 28:31
            bitset<4> op;
            op[0] = bits[28];
            op[1] = bits[29];
            op[2] = bits[30];
            op[3] = bits[31];

            unsigned long opcode = op.to_ulong();

            if (opcode == 0)
            {
                // The register A receives the value in register B, unless the register C contains 0.
                if (registers[C.to_ulong()] != 0)
                {
                    registers[A.to_ulong()] = registers[B.to_ulong()];
                }
            }
            else if (opcode == 1)
            {
                // The register A receives the value stored at offset in register C in the array identified by B.
                registers[A.to_ulong()] = arrays[registers[B.to_ulong()]][registers[C.to_ulong()]];
            }
            else if (opcode == 2)
            {
                // The array identified by A is updated at the offset in register B to store the value in register C.
                if (arrays.count(registers[A.to_ulong()]) == 0)
                {
                    printf("Array has not been allocated.\n");
                    exit(-1);
                }
                else if (registers[B.to_ulong()] >= arrays[registers[A.to_ulong()]].size())
                {
                    printf("Index is too large for array.\n");
                    exit(-1);
                }
                arrays[registers[A.to_ulong()]][registers[B.to_ulong()]] = registers[C.to_ulong()];
            }
            else if (opcode == 3)
            {
                // The register A receives the value in register B plus the value in register C, modulo 2^32.
                registers[A.to_ulong()] = registers[B.to_ulong()] + registers[C.to_ulong()];
            }
            else if (opcode == 4)
            {
                // The register A receives the value in register B times the value in register C, modulo 2^32
                registers[A.to_ulong()] = registers[B.to_ulong()] * registers[C.to_ulong()];
            }
            else if (opcode == 5)
            {
                // The register A receives the value in register B divided by the value in register C, if any,
                // where each quantity is treated as an unsigned 32-bit number.

                // If the program attempts to divide by 0, then the machine will Fail.
                if (registers[C.to_ulong()] == 0)
                {
                    printf("Attempted to divide by zero.\n");
                    exit(-1);
                }

                registers[A.to_ulong()] = registers[B.to_ulong()] / registers[C.to_ulong()];
            }
            else if (opcode == 6)
            {
                // Each bit in the register A receives the 1 bit if either register B or register C has a 0 bit in that position.
                // Otherwise the bit in register A receives the 0 bit.
                registers[A.to_ulong()] = ~(registers[B.to_ulong()] & registers[C.to_ulong()]);
            }
            else if (opcode == 7)
            {
                // The machine stops computation.
                printf("Halt.\n");
                exit(0);
            }
            else if (opcode == 8)
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

                    arrays[idx] = vector<word>(registers[C.to_ulong()], 0);
                    registers[B.to_ulong()] = idx;
                }
                else
                {
                    printf("Ran out of arrays to allocate.\n");
                    exit(-1);
                }
            }
            else if (opcode == 9)
            {
                // The array identified by the register C is deallocated (freed).
                // Future allocations may then reuse that identifier.
                if (registers[C.to_ulong()] == 0)
                {
                    // If the program attempts to deallocate the ’0’ array, or to
                    // deallocate an array that is not active, then the machine will Fail.
                    printf("Attempted to deallocate the '0' array.\n");
                    exit(-1);
                }
                else if (arrays.count(registers[C.to_ulong()]) == 0)
                {
                    printf("Attempted to deallocate unallocated array.\n");
                    exit(-1);
                }

                arrays.erase(registers[C.to_ulong()]);
                freeIdentifiers.push_back(registers[C.to_ulong()]);
            }
            else if (opcode == 10)
            {
                //  The value in the register C is displayed on the console. Only values in the range 0–255 are allowed.
                if (registers[C.to_ulong()] > 255)
                {
                    printf("Output was larger than 255.\n");
                    exit(-1);
                }
                cout << (char)registers[C.to_ulong()];
            }
            else if (opcode == 11)
            {
                // The machine waits for input on the console. When input arrives, the register C is loaded with the input, which
                // must be in the range 0–255. If the end of input has been signaled, then the register C is filled with all 1’s.
                if (cin.eof())
                {
                    registers[C.to_ulong()] = 0xFFFFFFFF;
                }
                else
                {
                    char input;
                    cin.get(input);
                    registers[C.to_ulong()] = (word)input;
                }
            }
            else if (opcode == 12)
            {
                // The array identified by the B register is duplicated and the duplicate replaces the ‘0’ array, regardless of size.
                // The program counter is updated to indicate the word of this array that is described by the offset given in C, where the
                // value 0 denotes the first word, 1 the second, etc.
                if (arrays.count(registers[B.to_ulong()]) == 0)
                {
                    printf("Unable to locate array to duplicate and load into '0'.\n");
                    exit(-1);
                }

                if (registers[B.to_ulong()] != 0)
                {
                    arrays[0] = arrays[registers[B.to_ulong()]];
                    /*arrays[0].resize(arrays[registers[B.to_ulong()]].size());
                    for (auto v = 0; v != arrays[registers[B.to_ulong()]].size(); ++v)
                    {
                        arrays[0][v] = arrays[registers[B.to_ulong()]][v];
                    }*/
                }

                if (registers[C.to_ulong()] >= arrays[0].size())
                {
                    printf("Program pointer is larger than program.\n");
                    exit(-1);
                }

                it = registers[C.to_ulong()] - 1;
            }
            else if (opcode == 13)
            {
                // The value in bits 0:24 is loaded into the register A (given by bits 25:27).
                bitset<3> A;
                A[0] = bits[25];
                A[1] = bits[26];
                A[2] = bits[27];
                registers[A.to_ulong()] = arrays[0][it] & 0x1FFFFFF;
            }
            else
            {
                // unrecognized opcode
                printf("Unrecognized opcode.\n");
                exit(-1);
            }
        }

        return 0;
    }
    else
    {
        return -1;
    }
}