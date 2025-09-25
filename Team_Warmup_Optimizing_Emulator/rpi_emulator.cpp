#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <cstring>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <string>
#include <unordered_map>
#include <vector>

using namespace std;

#ifdef DEBUG
// For timing measurements
using Clock = chrono::high_resolution_clock;
using Duration = chrono::nanoseconds;
#endif

typedef uint32_t word;
const int wordSize = sizeof(word);

int main(int argc, char *argv[]) {
  // initialize machine
  word registers[8] = {0};
  vector<vector<word>> arrays = {};
  vector<word> freeIdentifiers = {};

#ifdef DEBUG
  // Timing measurements
  vector<Duration> opTimes(14, Duration::zero());
  vector<uint64_t> opCounts(14, 0);
#endif

  // load program
  if (argc > 1) {
    // open the file:
    basic_ifstream<char> filestream(argv[1], ios::binary);

    if (!filestream) {
      // file not found
      exit(-1);
    }

    filestream.seekg(0, ios::end);
    size_t fileSize = filestream.tellg() / 4;
    filestream.seekg(0, ios::beg);

    arrays.emplace_back(vector<word>());
    word tempWord;
    for (auto i = 0; i < fileSize; ++i) {
      filestream.read(reinterpret_cast<char *>(&tempWord), wordSize);
      // Swap bytes from big to little endian
      tempWord = __builtin_bswap32(tempWord);
      arrays[0].emplace_back(tempWord);
    }
    filestream.close();

    // run
    word size = fileSize;
    for (word it = 0; it < size; ++it) {
      word bits = arrays[0][it];

      // The operation code is given by bits 28:31
      int op = bits >> 28;

#ifdef DEBUG
      Clock::time_point start;
#endif
      switch (op) {
      case 0: {
#ifdef DEBUG
        start = Clock::now();
#endif
        uint8_t A = (bits >> 6) & 7;
        uint8_t B = (bits >> 3) & 7;
        uint8_t C = bits & 7;
        // The register A receives the value in register B, unless the register
        // C contains 0.
        // if (registers[C] != 0 & A != B) {
        registers[C] ? registers[A] = registers[B] : registers[A];
        //}
#ifdef DEBUG
        opTimes[op] += Clock::now() - start;
        opCounts[op]++;
#endif
        break;
      }
      case 1: {
#ifdef DEBUG
        start = Clock::now();
#endif
        uint8_t A = (bits >> 6) & 7;
        uint8_t B = (bits >> 3) & 7;
        uint8_t C = bits & 7;
        // The register A receives the value stored at offset in register C in
        // the array identified by B.
        registers[A] = arrays[registers[B]][registers[C]];
#ifdef DEBUG
        opTimes[op] += Clock::now() - start;
        opCounts[op]++;
#endif
        break;
      }
      case 2: {
#ifdef DEBUG
        start = Clock::now();
#endif
        uint8_t A = (bits >> 6) & 7;
        uint8_t B = (bits >> 3) & 7;
        uint8_t C = bits & 7;
        // The array identified by A is updated at the offset in register B to
        // store the value in register C.
        arrays[registers[A]][registers[B]] = registers[C];
#ifdef DEBUG
        opTimes[op] += Clock::now() - start;
        opCounts[op]++;
#endif
        break;
      }
      case 3: {
#ifdef DEBUG
        start = Clock::now();
#endif
        uint8_t A = (bits >> 6) & 7;
        uint8_t B = (bits >> 3) & 7;
        uint8_t C = bits & 7;
        // The register A receives the value in register B plus the value in
        // register C, modulo 2^32.
        registers[A] = registers[B] + registers[C];
#ifdef DEBUG
        opTimes[op] += Clock::now() - start;
        opCounts[op]++;
#endif
        break;
      }
      case 4: {
#ifdef DEBUG
        start = Clock::now();
#endif
        uint8_t A = (bits >> 6) & 7;
        uint8_t B = (bits >> 3) & 7;
        uint8_t C = bits & 7;
        // The register A receives the value in register B times the value in
        // register C, modulo 2^32
        registers[A] = registers[B] * registers[C];
#ifdef DEBUG
        opTimes[op] += Clock::now() - start;
        opCounts[op]++;
#endif
        break;
      }
      case 5: {
#ifdef DEBUG
        start = Clock::now();
#endif
        uint8_t A = (bits >> 6) & 7;
        uint8_t B = (bits >> 3) & 7;
        uint8_t C = bits & 7;
        // The register A receives the value in register B divided by the value
        // in register C, if any, where each quantity is treated as an unsigned
        // 32-bit number.

        // If the program attempts to divide by 0, then the machine will Fail.
        registers[A] = registers[B] / registers[C];
#ifdef DEBUG
        opTimes[op] += Clock::now() - start;
        opCounts[op]++;
#endif
        break;
      }
      case 6: {
#ifdef DEBUG
        start = Clock::now();
#endif
        uint8_t A = (bits >> 6) & 7;
        uint8_t B = (bits >> 3) & 7;
        uint8_t C = bits & 7;
        // Each bit in the register A receives the 1 bit if either register B or
        // register C has a 0 bit in that position. Otherwise the bit in
        // register A receives the 0 bit.
        registers[A] = ~(registers[B] & registers[C]);
#ifdef DEBUG
        opTimes[op] += Clock::now() - start;
        opCounts[op]++;
#endif
        break;
      }
      case 7: {
#ifdef DEBUG
        // Print timing statistics
        cout << "\nTiming Statistics:\n";
        cout << fixed << setprecision(3);
        for (size_t i = 0; i < 14; i++) {
          if (opCounts[i] > 0) {
            double mean_ns =
                chrono::duration_cast<Duration>(opTimes[i]).count() /
                static_cast<double>(opCounts[i]);
            cout << "Opcode " << i << ": " << mean_ns << " ns (avg), "
                 << opCounts[i] << " calls,\t"
                 << chrono::duration_cast<chrono::seconds>(opTimes[i]).count()
                 << " s total\n";
          }
        }
#endif
        // The machine stops computation.
        exit(0);
      }
      case 8: {
#ifdef DEBUG
        start = Clock::now();
#endif
        uint8_t B = (bits >> 3) & 7;
        uint8_t C = bits & 7;
        // A new array is created; the value in the register C gives the number
        // of words in the new array. This new array is zero-initialized. A bit
        // pattern not consisting of exclusively the 0 bit, and that identifies
        // no other active allocated array, is placed in the B register, and it
        // identifies the new array.
        if (freeIdentifiers.size()) {
          word idx = freeIdentifiers.back();
          freeIdentifiers.pop_back();
          arrays[idx] = vector<word>(registers[C], 0);
          registers[B] = idx;
        } else {
          arrays.emplace_back(vector<word>(registers[C], 0));
          registers[B] = arrays.size() - 1;
        }
#ifdef DEBUG
        opTimes[op] += Clock::now() - start;
        opCounts[op]++;
#endif
        break;
      }
      case 9: {
#ifdef DEBUG
        start = Clock::now();
#endif
        uint8_t C = bits & 7;
        // The array identified by the register C is deallocated (freed).
        // Future allocations may then reuse that identifier.

        // Free memory in constant time
        // vector<word>().swap(arrays[registers[C]]); // Free memory
        // arrays.erase(registers[C]);
        freeIdentifiers.emplace_back(registers[C]);
#ifdef DEBUG
        opTimes[op] += Clock::now() - start;
        opCounts[op]++;
#endif
        break;
      }
      case 10: {
#ifdef DEBUG
        start = Clock::now();
#endif
        uint8_t C = bits & 7;
        //  The value in the register C is displayed on the console. Only values
        //  in the range 0–255 are allowed.
        cout << (char)registers[C];
#ifdef DEBUG
        opTimes[op] += Clock::now() - start;
        opCounts[op]++;
#endif
        break;
      }
      case 11: {
        uint8_t C = bits & 7;
#ifdef DEBUG
        start = Clock::now();
#endif
        // The machine waits for input on the console. When input arrives, the
        // register C is loaded with the input, which must be in the range
        // 0–255. If the end of input has been signaled, then the register C is
        // filled with all 1’s.
        if (cin.eof()) {
          registers[C] = 0xFFFFFFFF;
        } else {
          char input;
          cin.get(input);
          registers[C] = (word)input;
        }
#ifdef DEBUG
        opTimes[op] += Clock::now() - start;
        opCounts[op]++;
#endif
        break;
      }
      case 12: {
#ifdef DEBUG
        start = Clock::now();
#endif
        uint8_t B = (bits >> 3) & 7;
        uint8_t C = bits & 7;
        // The array identified by the B register is duplicated and the
        // duplicate replaces the ‘0’ array, regardless of size. The program
        // counter is updated to indicate the word of this array that is
        // described by the offset given in C, where the value 0 denotes the
        // first word, 1 the second, etc.
        if (registers[B] != 0) {
          arrays[0] = arrays[registers[B]];
          size = arrays[0].size();
        }
        it = registers[C] - 1;
#ifdef DEBUG
        opTimes[op] += Clock::now() - start;
        opCounts[op]++;
#endif
        break;
      }
      case 13: {
#ifdef DEBUG
        start = Clock::now();
#endif
        // The value in bits 0:24 is loaded into the register A (given by bits
        // 25:27).
        uint8_t A = (bits >> 25) & 7;
        registers[A] = bits & 0x01FFFFFF;
#ifdef DEBUG
        opTimes[op] += Clock::now() - start;
        opCounts[op]++;
#endif
        break;
      }
      default:
        // unrecognized opcode
        exit(-1);
        break;
      }
    }
    return 0;
  } else {
    return -1;
  }
}