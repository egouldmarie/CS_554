#include <iostream>
#include <cstring>
#include <chrono>
#include "um.hpp"

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <program.um>" << std::endl;
        return 1;
    }

    try {
        UniversalMachine um;
        um.loadProgram(argv[1]);

        auto start = std::chrono::high_resolution_clock::now();
        um.run();
        auto end = std::chrono::high_resolution_clock::now();

        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
        std::cout << "\nExecution time: " << duration.count() << " ms" << std::endl;
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}
