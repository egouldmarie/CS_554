#include <iostream>
#include <iomanip>
#include <fstream>
#include <bitset>
#include <vector>
#include <map>

using namespace std;

typedef uint32_t word;
const int wordSize = sizeof(word);

struct mach
{
    word registers[8] = {0};
    map<word, vector<word>> arrays = {};
    vector<word> freeIdentifiers = {};
};

map<u_long, string>
    opcodes = {
        {0, "Reg[C] !=0 ? Reg[A] <- Reg[B]"},
        {1, "Reg[A] <- Array[ Reg[B] ][ Reg[C] ]"},
        {2, "Array[ Reg[A] ][ Reg[B] ] <- Reg[C]"},
        {3, "Reg[A] <- (Reg[B] + Reg[C]) % 2^32"},
        {4, "Reg[A] <- (Reg[B] * Reg[C]) % 2^32"},
        {5, "Reg[A] <- Reg[B] / Reg[C]"},
        {6, "Reg[A] <- !(Reg[B] & Reg[C])"},
        {7, "Halt"},
        {8, "idx = pop from free identifiers, Reg[B] <- idx, Array[idx] <- <Reg[C]>"},
        {9, "Free Array[ Reg[C] ]"},
        {10, "Output <- Reg[C]"},
        {11, "0 <= Reg[C] <= 255 ? Input -> Reg[C]"},
        {12, "Array[0] <- Array[ Reg[B] ], pointer <- Reg[C]"},
        {13, "Reg[bits(25:27)] <- bits(0:24)"}};

bool debug = false;

int main(int argc, char *argv[])
{
    // cout << "0x00000000\n";

    // initialize machine
    mach machine;

    // load program
    if (argc > 1)
    {
        string output = "";

        // open the file:
        basic_ifstream<char> filestream(argv[1], ios::binary);
        word tempWord;

        if (!filestream)
        {
            printf("File not found.\n");
            exit(-1);
        }

        while (!filestream.eof())
        {
            filestream.read(reinterpret_cast<char *>(&tempWord), wordSize);
            machine.arrays[0].emplace_back(((0xFF000000 & tempWord) >> 24) |
                                           ((0x00FF0000 & tempWord) >> 8) |
                                           ((0x0000FF00 & tempWord) << 8) |
                                           ((0x000000FF & tempWord) << 24));
        }
        filestream.close();

        if (debug)
        {
            output += "\nSETUP\n";
            output += "Reg[0]: " + to_string(machine.registers[0]);
            for (int j = 1; j < 7; ++j)
            {
                output += "Reg[" + to_string(j) + "]: " + to_string(machine.registers[j]) + ", ";
            }
            output += "Reg[7]: " + to_string(machine.registers[7]) + "\n";
            output += "Array[0]: <" + to_string(machine.arrays[0].size()) + ">";
            output += "\n\n                                             START                                             \n";
            output += "-----------------------------------------------------------------------------------------------\n";
            cout << output;
        }

        // run
        for (auto it = 0; it < machine.arrays[0].size(); ++it)
        {
            bitset<32> bits = machine.arrays[0][it]; //*it;

            // Standard instructions use three registers, A,
            // B, and C. Each register is described by a three
            // bit segment of the instruction. Register A is
            // given by bits 6:8, B is given by bits 3:5, and
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

            int opcode = bits[28] + bits[29] * 2 + bits[30] * 2 * 2 + bits[31] * 2 * 2 * 2;

            // debug print statement
            if (debug)
            {
                printf("-----------------------------------------------------------------------------------------------\n");
                printf("--> Array[0][%d]\n", it);
                printf("opcode %d:\t%s\n", opcode, opcodes[opcode].c_str());
                if (opcode <= 12)
                {
                    printf("\t\tReg[A=%lu]: %u,\tReg[B=%lu]: %u,\tReg[C=%lu]: %u\n", A.to_ulong(), machine.registers[A.to_ulong()], B.to_ulong(), machine.registers[B.to_ulong()], C.to_ulong(), machine.registers[C.to_ulong()]);
                }
            }

            if (opcode == 0)
            {
                // The register A receives the value in register B,
                // unless the register C contains 0.
                if (machine.registers[C.to_ulong()] > 0)
                {
                    machine.registers[A.to_ulong()] = machine.registers[B.to_ulong()];
                    // memcpy(&machine.registers[A.to_ulong()], &machine.registers[B.to_ulong()], wordSize);
                }
                if (debug)
                {
                    printf("\t%u != 0 ? Reg[%lu] <- %u\n", machine.registers[C.to_ulong()], A.to_ulong(), machine.registers[B.to_ulong()]);
                }
            }
            else if (opcode == 1)
            {
                // The register A receives the value stored at offset
                // in register C in the array identified by B.
                machine.registers[A.to_ulong()] = machine.arrays[machine.registers[B.to_ulong()]][machine.registers[C.to_ulong()]];
                // memcpy(&machine.registers[A.to_ulong()], &machine.arrays[machine.registers[B.to_ulong()]][machine.registers[C.to_ulong()]], wordSize);
                if (debug)
                {
                    printf("\tReg[%lu] <- %u\n", A.to_ulong(), machine.arrays[machine.registers[B.to_ulong()]][machine.registers[C.to_ulong()]]);
                }
            }
            else if (opcode == 2)
            {
                // The array identified by A is updated at the offset
                // in register B to store the value in register C.
                if (machine.arrays.count(machine.registers[A.to_ulong()]) == 0)
                {
                    printf("Array has not been allocated.\n");
                    exit(-1);
                }
                else if (machine.registers[B.to_ulong()] >= machine.arrays[machine.registers[A.to_ulong()]].size())
                {
                    printf("Index is too large for array.\n");
                    exit(-1);
                }
                machine.arrays[machine.registers[A.to_ulong()]][machine.registers[B.to_ulong()]] = machine.registers[C.to_ulong()];
                // memcpy(&machine.arrays[machine.registers[A.to_ulong()]][machine.registers[B.to_ulong()]], &machine.registers[C.to_ulong()], wordSize);
                if (debug)
                {
                    printf("\tArray[%u][%u] <- %u\n", machine.registers[A.to_ulong()], machine.registers[B.to_ulong()], machine.registers[C.to_ulong()]);
                }
            }
            else if (opcode == 3)
            {
                // The register A receives the value in register B plus
                // the value in register C, modulo 2^32.
                word b = machine.registers[B.to_ulong()];
                word c = machine.registers[C.to_ulong()];
                machine.registers[A.to_ulong()] = b + c;
                if (debug)
                {
                    printf("\tReg[%lu] <- (%u + %u) %% 2^32 = %u\n", A.to_ulong(), b, c, machine.registers[A.to_ulong()]);
                }
            }
            else if (opcode == 4)
            {
                // The register A receives the value in register B times
                // the value in register C, modulo 2^32.
                machine.registers[A.to_ulong()] = machine.registers[B.to_ulong()] * machine.registers[C.to_ulong()];
                if (debug)
                {
                    printf("\tReg[%lu] <- (%u * %u) %% 2^32 = %u\n", A.to_ulong(), machine.registers[B.to_ulong()], machine.registers[C.to_ulong()], machine.registers[A.to_ulong()]);
                }
            }
            else if (opcode == 5)
            {
                // The register A receives the value in register B divided
                // by the value in register C, if any, where each quantity
                // is treated as an unsigned 32-bit number.

                // If the program attempts to divide by 0, then the machine will Fail.
                if (machine.registers[C.to_ulong()] == 0)
                {
                    printf("Attempted to divide by zero.\n");
                    exit(-1);
                }

                machine.registers[A.to_ulong()] = machine.registers[B.to_ulong()] / machine.registers[C.to_ulong()];
                if (debug)
                {
                    printf("\tReg[%lu] <- %u / %u = %u\n", A.to_ulong(), machine.registers[B.to_ulong()], machine.registers[C.to_ulong()], machine.registers[A.to_ulong()]);
                }
            }
            else if (opcode == 6)
            {
                // Each bit in the register A receives the 1 bit if either
                // register B or register C has a 0 bit in that position.
                // Otherwise the bit in register A receives the 0 bit.
                bitset<32> b = machine.registers[B.to_ulong()];
                bitset<32> c = machine.registers[C.to_ulong()];

                machine.registers[A.to_ulong()] = (word)((~(b & c)).to_ulong());
                if (debug)
                {
                    cout << "\tReg[" << A.to_ulong() << "] <- !(" << b << " & " << c << ") = " << (bitset<32>)machine.registers[A.to_ulong()] << "\n";
                }
            }
            else if (opcode == 7)
            {
                // The machine stops computation.
                printf("Halt.\n");
                exit(0);
            }
            else if (opcode == 8)
            {
                // A new array is created; the value in the register C gives
                // the number of words in the new array. This new array is
                // zero-initialized. A bit pattern not consisting of exclusively
                // the 0 bit, and that identifies no other active allocated array,
                // is placed in the B register, and it identifies the new array.

                if (machine.arrays.size() < 0xFFFFFFFF)
                {
                    word idx;
                    if (machine.freeIdentifiers.size() > 0)
                    {
                        idx = machine.freeIdentifiers.back();
                        machine.freeIdentifiers.pop_back();
                    }
                    else
                    {
                        for (word id = machine.arrays.size(); id < 0xFFFFFFFF; ++id)
                        {
                            if (machine.arrays.count(id) == 0)
                            {
                                idx = id;
                                break;
                            }
                        }
                    }

                    machine.registers[B.to_ulong()] = idx;
                    machine.arrays[idx] = vector<word>(machine.registers[C.to_ulong()]);
                }
                else
                {
                    printf("Ran out of arrays to allocate.\n");
                    exit(-1);
                }
                if (debug)
                {
                    printf("\t\tidx = %u, Reg[%lu] <- %u, Array[%u] <- <%u>\n", machine.registers[B.to_ulong()], B.to_ulong(), machine.registers[B.to_ulong()], machine.registers[B.to_ulong()], machine.registers[C.to_ulong()]);
                }
                // cout << "\x1b[A" << "0x" << hex << setw(8) << setfill('0') << machine.arrays.size() << "\n";
            }
            else if (opcode == 9)
            {
                // printf("opcode: %d, free array at index in C: %u\n", opcode, machine.registers[C.to_ulong()]);

                // The array identified by the register C is deallocated (freed).
                // Future allocations may then reuse that identifier.
                if (machine.registers[C.to_ulong()] == 0)
                {
                    // If the program attempts to deallocate the ’0’ array, or to
                    // deallocate an array that is not active, then the machine will Fail.
                    printf("Attempted to deallocate the '0' array.\n");
                    exit(-1);
                }
                else if (machine.arrays.count(machine.registers[C.to_ulong()]) == 0)
                {
                    printf("Attempted to deallocate unallocated array.\n");
                    exit(-1);
                }

                machine.arrays.erase(machine.registers[C.to_ulong()]);
                machine.freeIdentifiers.emplace_back(machine.registers[C.to_ulong()]);
                if (debug)
                {
                    printf("\t\tFree Array[ %u ]\n", machine.registers[C.to_ulong()]);
                }
            }
            else if (opcode == 10)
            {
                //  The value in the register C is displayed on the console.
                //  Only values in the range 0–255 are allowed.
                if (machine.registers[C.to_ulong()] > 255)
                {
                    printf("Output was larger than 255.\n");
                    exit(-1);
                }
                cout << (char)machine.registers[C.to_ulong()];
                if (debug)
                {
                    printf("\t\tOutput <- %c\n", (char)machine.registers[C.to_ulong()]);
                }
            }
            else if (opcode == 11)
            {
                // The machine waits for input on the console. When input
                // arrives, the register C is loaded with the input, which
                // must be in the range 0–255. If the end of input has been
                // signaled, then the register C is filled with all 1’s.
                if (cin.eof())
                {
                    machine.registers[C.to_ulong()] = 0xFFFFFFFF;
                }
                else
                {
                    char input;
                    cin.get(input);
                    machine.registers[C.to_ulong()] = input;
                }
            }
            else if (opcode == 12)
            {
                // The array identified by the B register is duplicated and
                // the duplicate replaces the ‘0’ array, regardless of size.
                // The program counter is updated to indicate the word of this
                // array that is described by the offset given in C, where the
                // value 0 denotes the first word, 1 the second, etc.
                if (machine.arrays.count(machine.registers[B.to_ulong()]) == 0)
                {
                    printf("Unable to locate array to duplicate and load into '0'.\n");
                    exit(-1);
                }

                if (machine.registers[B.to_ulong()] != 0)
                {
                    machine.arrays[0] = machine.arrays[machine.registers[B.to_ulong()]];
                    /*machine.arrays[0].clear();
                    for (auto v = machine.arrays[machine.registers[B.to_ulong()]].begin(); v != machine.arrays[machine.registers[B.to_ulong()]].end(); ++v)
                    {
                        machine.arrays[0].emplace_back(*v);
                    }*/
                }

                if (machine.registers[C.to_ulong()] >= machine.arrays[0].size())
                {
                    printf("Program pointer is larger than program.\n");
                    exit(-1);
                }

                it = machine.registers[C.to_ulong()] - 1;
            }
            else if (opcode == 13)
            {
                // The value in bits 0:24 is loaded into the register A
                // (given by bits 25:27).
                A[0] = bits[25];
                A[1] = bits[26];
                A[2] = bits[27];
                machine.registers[A.to_ulong()] = (word)(bits & (bitset<32>)0x3FFFFF).to_ulong();
                if (debug)
                {
                    printf("\t\tbits(25:27) = %lu,  bits(0:24) = %u\n", A.to_ulong(), machine.registers[A.to_ulong()]);
                    printf("\t\tReg[%lu] <- %u\n", A.to_ulong(), machine.registers[A.to_ulong()]);
                }
            }
            else
            {
                // unrecognized opcode
                printf("Unrecognized opcode.\n");
                exit(-1);
            }
            if (debug)
            {
                printf("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n");
                printf("Reg[0]: %u, Reg[1]: %u, Reg[2]: %u, Reg[3]: %u, Reg[4]: %u, Reg[5]: %u, Reg[6]: %u, Reg[7]: %u\n", machine.registers[0], machine.registers[1], machine.registers[2], machine.registers[3], machine.registers[4], machine.registers[5], machine.registers[6], machine.registers[7]);
                // printf("Number of Arrays: %zu", machine.arrays.size());
                printf("Array[0]<%zu>", machine.arrays[0].size());
                for (auto i = 1; i < machine.arrays.size(); ++i)
                {
                    printf("\nArray[%d]<%zu>:", i, machine.arrays[i].size());
                }
                printf("\n");
            }
        }

        return 0;
    }
    else
    {
        return -1;
    }
}