/*
* CS554 Fall 2025 Week 2 Emulator Warmup in C
* See instructions.h for non-memory instructions
* Author: Nathan J. Rowe
* Email: nrowe1@unm.edu
* UNM ID: 101992706
*
* TODO: - Track deallocated memory slots
*       - Move memory manipulating operations to instructions.h
*       - Make it faster
*/

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include "instructions.h"

/* START REGISTERS */
#define NUM_REGISTERS 8
uint32_t reg[NUM_REGISTERS] = {0};
/* END REGISTERS */

/* START MEMORY */
// Initial size of the memory array
// Starting size, optimized to reduce resize_memory calls in the sandmark test
uint32_t memory_size = 768; 
// Array to track the size of each memory array
// I need this to hard copy arrays to the zero array since sandmark hates reference passing
size_t* array_sizes;
uint32_t** memory;



// Resize of the memory array
uint32_t** resize_memory(uint32_t** memory, size_t prev_size) {
    size_t new_size = prev_size * 2;
    uint32_t** new_memory = (uint32_t**)malloc(new_size * sizeof(uint32_t*));
    if (!new_memory) {
        perror("Failed to allocate memory for new memory array");
        exit(EXIT_FAILURE);
    }
    // Resize the array_sizes to match the new memory size
    array_sizes = (size_t*)realloc(array_sizes, new_size * sizeof(size_t));
    if (!array_sizes) {
        perror("Failed to allocate memory for array sizes");
        free(new_memory);
        exit(EXIT_FAILURE);
    }
    memory_size = new_size;
    // Copy old memory contents
    for (size_t i = 0; i < new_size; i++) {
        if (i < prev_size && memory[i]) {
            new_memory[i] = memory[i];
        } else {
            new_memory[i] = NULL;
            array_sizes[i] = 0;
        }
    }
    free(memory);
    return new_memory;
}

/* END MEMORY */

int run() {
    // Main loop to execute instructions
    uint32_t pc = 0; // Program counter

    // Register bits
    uint32_t a;
    uint32_t b;
    uint32_t c;

    // Temporary variables for instruction decoding
    uint32_t opcode;
    uint32_t instruction;
    // Used to manage memory allocation
    size_t index = 1;
    
    while (1) {
        instruction = memory[0][pc++];
        opcode = instruction >> 28;

        if (opcode < 13 && opcode >= 0) { // Standard instruction
            a = (instruction & 0x000001E0) >> 6;
            b = (instruction & 0x00000038) >> 3;
            c = (instruction & 0x00000007);
        }
        else if (opcode == 13) { // Load immediate
            a = (instruction & 0x0E000000) >> 25; 
            b = (instruction & 0x01FFFFFF);
        }
        else { //standard instruction
           fprintf(stderr, "Invalid opcode: %u at instruction %d\n", opcode, pc);
           return EXIT_FAILURE;
        }
       
        // Execute the instruction based on the opcode
        switch (opcode) {
            case 0: 
                conditional_move(&reg[a], &reg[b], &reg[c]);
                break;
            case 1:
                reg[a] = memory[reg[b]][reg[c]];
                break;
            case 2: 
                memory[reg[a]][reg[b]] = reg[c];
                break;
            case 3: 
                addition(&reg[a], &reg[b], &reg[c]);
                break;
            case 4: 
                multiplication(&reg[a], &reg[b], &reg[c]);
                break;
            case 5: 
                division(&reg[a], &reg[b], &reg[c]);
                break;
            case 6: 
                nand(&reg[a], &reg[b], &reg[c]);
                break;
            case 7:
                return EXIT_SUCCESS;
                break;
            case 8:
                // Resize memory if needed
                if (index >= memory_size) {
                    memory = resize_memory(memory, memory_size);
                }
                memory[index] = (uint32_t*)calloc(reg[c], 4);
                if (!memory[index]) {
                    perror("Failed to allocate memory for new array");
                    return EXIT_FAILURE;
                }
                array_sizes[index] = reg[c]; // Track the size
                reg[b] = index;
                index++;
                break;
            case 9: 
                free(memory[reg[c]]);
                memory[reg[c]] = NULL; // Mark as deallocated
                break;
            case 10: 
                output(&reg[c]);
                break;
            case 11:
                unsigned char buffer[4];
                fread(buffer+3, 1, 1, stdin);
                reg[c] = buffer[3];
                break;
            case 12: 
                pc = reg[c];
                if (reg[b] != 0) {
                    if (memory[reg[b]] == NULL) {
                        fprintf(stderr, "Program not found in memory\n");
                        return EXIT_FAILURE;
                    }
                    // Replace zero array with new program
                    free(memory[0]);
                    memory[0] = (uint32_t*)malloc(array_sizes[reg[b]] * 4);
                    if (!memory[0]) {
                        perror("Failed to allocate memory for program copy");
                        return EXIT_FAILURE;
                    }
                    memcpy(memory[0], memory[reg[b]], array_sizes[reg[b]] * 4);
                    // Update the size of memory[0]
                    array_sizes[0] = array_sizes[reg[b]];
                }
                break;
            case 13: 
                load_immediate(&reg[a], &b);
                break;
            default: 
                fprintf(stderr, "Unknown opcode: %u\n", opcode);
                return EXIT_FAILURE;
        }
    }
    return EXIT_SUCCESS;
}

int main(int argc, char *argv[]) {

    /* Memory Initialization */
    memory = (uint32_t**)calloc(memory_size, sizeof(uint32_t*));
    if (!memory) {
        perror("Failed to allocate memory for memory array");
        exit(EXIT_FAILURE);
    }
    array_sizes = (size_t*)calloc(memory_size, sizeof(size_t));
    if (!array_sizes) {
        perror("Failed to allocate memory for array sizes");
        free(memory);
        exit(EXIT_FAILURE);
    }

    /* Read input */
    FILE *file = fopen(argv[1], "rb");
    
    if (!file) {
        perror("Failed to open file");
        return EXIT_FAILURE;
    }

    // Determine file size
    // START LLM GENERATED
    /* ChatGPT 4.1, free used with the 'Web Search' setting enabled
    *  https://chatgpt.com/share/68ad2341-f5ac-8011-88b8-ea2ba73cbdcb
    * Prompt: Assume I was working with a word size of uint32_t in C. How can I determine the number of words in a file?
    * Suggestion summarized from:  https://stackoverflow.com/questions/30853210/count-number-of-32-bit-numbers-in-binary-file?utm_source=chatgpt.com
    */
    fseek(file, 0, SEEK_END);
    long file_size = ftell(file);
    fseek(file, 0, SEEK_SET);
    size_t num_words = file_size / 4;

    //END LLM GENERATED

    // Supply contents of the file to memory[0]
    memory[0] = (uint32_t*)malloc(num_words * 4);
    fread(memory[0], 4, num_words, file);
     // Don't need the file anymore :)
    fclose(file);

    // Store the size of the initial program
    array_sizes[0] = num_words;

    // Convert all values to big endian
    // Taking advantage of the optimized, gcc builtin function
    // Suggested in https://stackoverflow.com/questions/19275955/convert-little-endian-to-big-endian
    for (size_t i = 0; i < num_words; i++) {
        memory[0][i] = __builtin_bswap32(memory[0][i]);
    }

    int result = run();
    return result;
}