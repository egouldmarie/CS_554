cmake_minimum_required(VERSION 3.14)
project(UniversalMachine)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Add compiler optimizations and warnings
if(MSVC)
    add_compile_options(/W4 /O2 /Oi /GL /arch:AVX2)
    add_link_options(/LTCG)
else()
    add_compile_options(-Wall -Wextra -Wpedantic -O3 -march=native -ffast-math)
    add_link_options(-flto)
endif()

# Add source files
add_executable(um
    src/main.cpp
    src/um.cpp
    src/memory.cpp
    src/instruction.cpp
)

# Include directories
target_include_directories(um PRIVATE include)