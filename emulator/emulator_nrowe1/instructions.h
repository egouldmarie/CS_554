/*
* CS554 Fall 2025 Week 2 Emulator Warmup in C
* Contains code for opcodes 0, 3, 4, 5, 6, 10, 11, and 13
* All memory access opcodes are handled by their switch statements in um.c
* "Why aren't all opcode functions in here?" Great question! Let's set that as
* a goal for Warmup 3
* Author: Nathan J. Rowe
* Email: nrowe1@unm.edu
* UNM ID: 101992706
*/

#ifndef INSTRUCTIONS_H
#define INSTRUCTIONS_H
#include <stdint.h>
#include <stdio.h>
#include <string.h>
//Opcode 0
// Conditional Move
void conditional_move(uint32_t *a, uint32_t *b, uint32_t *c) {
    *a = *c ? *b : *a;
}

/*
//Opcode 1
// Array Index
void array_index(uint32_t **memory, uint32_t *a, uint32_t *b, uint32_t *c) {
    if (*b >= *get_memory_size() || memory[*b] == NULL) {
        fprintf(stderr, "Array index not found in memory\n");
        exit(EXIT_FAILURE);
    }
    if (*c >= get_array_size(*b)) {
        fprintf(stderr, "Array index out of bounds: %u\n", *c);
        exit(EXIT_FAILURE);
    }
    *a = memory[*b][*c];
}
*/

/*
//Opcode 2
// Array Update
void array_update(uint32_t** memory, uint32_t *a, uint32_t *b, uint32_t *c) {
    if (*a >= *get_memory_size() || memory[*a] == NULL) {
        fprintf(stderr, "Array not found in memory\n");
        exit(EXIT_FAILURE);
    }
    if (*b >= get_array_size(*a)) {
        fprintf(stderr, "Array index out of bounds: %u\n", *b);
        exit(EXIT_FAILURE);
    }
    memory[*a][*b] = *c;
}
    */

//Opcode 3
// Addition
void addition(uint32_t *a, uint32_t *b, uint32_t *c) {
    *a = *b + *c;
}

//Opcode 4
// Multiplication
void multiplication(uint32_t *a, uint32_t *b, uint32_t *c) {
    *a = *b * *c;
}

//Opcode 5
// Division
void division(uint32_t *a, uint32_t *b, uint32_t *c) {
    if (*c == 0) {
        fprintf(stderr, "Division by zero error\n");
        exit(EXIT_FAILURE);
    }
    *a = *b / *c;
}

//Opcode 6
// Nand
void nand(uint32_t *a, uint32_t *b, uint32_t *c) {
    *a = ~(*b & *c);
}

/*
//Opcode 7
// Halt
void halt(uint32_t** memory, size_t* array_sizes) {
    break;
}
*/

/*
//Opcode 8
// Allocation
uint32_t** allocation(uint32_t** memory, size_t *index, uint32_t *c, uint32_t *b) {
    // Resize memory if needed
    if (*index >= *get_memory_size() / 2) {
        memory = resize_memory(memory, *get_memory_size());
    }
    memory[*index] = (uint32_t*)malloc(*c * sizeof(uint32_t));
    //Zero initialize the new array
    memset(memory[*index], 0, *c * sizeof(uint32_t));
    set_array_size(*index, *c); // Track the size
    *b = *index;
    (*index)++;
    return memory;
}
*/

/*
//Opcode 9
// Deallocation
void deallocation(uint32_t** memory, uint32_t *c) {
    if (*c >= *get_memory_size() || memory[*c] == NULL) {
        fprintf(stderr, "Array not found in memory for deallocation\n");
        exit(EXIT_FAILURE);
    }
    free(memory[*c]);
    memory[*c] = NULL; // Mark as deallocated
}
*/

//Opcode 10
// Output
void output(uint32_t *c) {
    if (*c > 255) {
        fprintf(stderr, "Output value out of range: %u\n", *c);
        return;
    }
    putchar((char)(*c));
}

//Opcode 11
// Input
void input(uint32_t *c) {
    unsigned char ch;
    fread(&ch, 1, 1, stdin);
    *c = ch;
}

/*
//Opcode 12
// Load Program
void load_program(uint32_t** memory, uint32_t *pc, uint32_t *b, uint32_t *c) {
    printf("[DEBUG] load_program: setting pc from %u to %u\n", *pc, *c);
    *pc = *c;
    if (*b != 0) {
        printf("[DEBUG] load_program: loading program from array %u\n", *b);
        if (*b >= *get_memory_size() || memory[*b] == NULL) {
            fprintf(stderr, "Program not found in memory\n");
            exit(EXIT_FAILURE);
        }
        uint32_t* program = memory[*b];
        // Get the size of the program array
        size_t program_size = get_array_size(*b);
        printf("[DEBUG] load_program: program size = %zu\n", program_size);
        
        //Replace memory[0] with the program
        free(memory[0]);
        memory[0] = (uint32_t*)malloc(program_size * sizeof(uint32_t));
        if (!memory[0]) {
            fprintf(stderr, "Failed to allocate memory for program copy\n");
            exit(EXIT_FAILURE);
        }
        memcpy(memory[0], program, program_size * sizeof(uint32_t));
        
        // Update the size of memory[0]
        set_array_size(0, program_size);
        printf("[DEBUG] load_program: updated array_sizes[0] to %zu\n", program_size);
    }
}
*/
//Opcode 13
// Load Immediate
void load_immediate(uint32_t *a, uint32_t *remainder) {
    *a = *remainder;
}
#endif