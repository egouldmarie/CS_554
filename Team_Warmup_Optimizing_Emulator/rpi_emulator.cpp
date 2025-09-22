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
    uint32_t numArrays = 0;

    // load program
    if (argc > 1)
    {
        // open the file:
        basic_ifstream<char> filestream(argv[1], ios::binary);

        if (!filestream)
        {
            // file not found
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

        uint32_t endIt = fileSize;

        // run
        for (uint32_t it = 0; it < endIt; ++it)
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

            switch (opcode)
            {
            case 0:
                // The register A receives the value in register B, unless the register C contains 0.
                if (registers[C.to_ulong()] != 0)
                {
                    registers[A.to_ulong()] = registers[B.to_ulong()];
                }
                break;
            case 1:
                // The register A receives the value stored at offset in register C in the array identified by B.
                registers[A.to_ulong()] = arrays[registers[B.to_ulong()]][registers[C.to_ulong()]];
                break;
            case 2:
                // The array identified by A is updated at the offset in register B to store the value in register C.
                arrays[registers[A.to_ulong()]][registers[B.to_ulong()]] = registers[C.to_ulong()];
                break;
            case 3:
                // The register A receives the value in register B plus the value in register C, modulo 2^32.
                registers[A.to_ulong()] = registers[B.to_ulong()] + registers[C.to_ulong()];
                break;
            case 4:
                // The register A receives the value in register B times the value in register C, modulo 2^32
                registers[A.to_ulong()] = registers[B.to_ulong()] * registers[C.to_ulong()];
                break;
            case 5:
                // The register A receives the value in register B divided by the value in register C, if any,
                // where each quantity is treated as an unsigned 32-bit number.
                registers[A.to_ulong()] = registers[B.to_ulong()] / registers[C.to_ulong()];
                break;
            case 6:
                // Each bit in the register A receives the 1 bit if either register B or register C has a 0 bit in that position.
                // Otherwise the bit in register A receives the 0 bit.
                registers[A.to_ulong()] = ~(registers[B.to_ulong()] & registers[C.to_ulong()]);
                break;
            case 7:
                // The machine stops computation.
                exit(0);
                break;
            case 8:
                // A new array is created; the value in the register C gives the number of words in the new array. This new array is
                // zero-initialized. A bit pattern not consisting of exclusively the 0 bit, and that identifies no other active allocated array,
                // is placed in the B register, and it identifies the new array.
                if (numArrays < 0xFFFFFFFF)
                {
                    word idx;
                    if (freeIdentifiers.begin() != freeIdentifiers.end())
                    {
                        idx = freeIdentifiers.back();
                        freeIdentifiers.pop_back();
                    }
                    else
                    {
                        for (word id = numArrays; id < 0xFFFFFFFF; ++id)
                        {
                            if (arrays.count(id) == 0)
                            {
                                idx = id;
                                break;
                            }
                        }
                    }

                    arrays[idx] = vector<word>(registers[C.to_ulong()]);
                    registers[B.to_ulong()] = idx;
                    ++numArrays;
                }
                else
                {
                    // ran out of arrays to allocate
                    exit(-1);
                }
                break;
            case 9:
                // The array identified by the register C is deallocated (freed).
                // Future allocations may then reuse that identifier.
                arrays.erase(registers[C.to_ulong()]);
                freeIdentifiers.push_back(registers[C.to_ulong()]);
                --numArrays;
                break;
            case 10:
                //  The value in the register C is displayed on the console. Only values in the range 0–255 are allowed.
                cout << (char)registers[C.to_ulong()];
                break;
            case 11:
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
                break;
            case 12:
                // The array identified by the B register is duplicated and the duplicate replaces the ‘0’ array, regardless of size.
                // The program counter is updated to indicate the word of this array that is described by the offset given in C, where the
                // value 0 denotes the first word, 1 the second, etc.
                if (registers[B.to_ulong()] != 0)
                {
                    arrays[0] = arrays[registers[B.to_ulong()]];
                    endIt = arrays[0].size();
                }

                it = registers[C.to_ulong()] - 1;
                break;
            case 13:
                // The value in bits 0:24 is loaded into the register A (given by bits 25:27).
                A[0] = bits[25];
                A[1] = bits[26];
                A[2] = bits[27];
                registers[A.to_ulong()] = arrays[0][it] & 0x1FFFFFF;
                break;
            default:
                // unrecognized opcode
                exit(-1);
                break;
            }
        }

        return 0;
    }
    else
    {
        return -1;
    }
}