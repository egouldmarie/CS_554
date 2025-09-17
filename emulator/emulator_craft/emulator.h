/* emulator.h Function Declarations */

#ifndef EMULATOR_H
#define EMULATOR_H

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include "uint32_stack.h"

typedef struct {
    uint32_t id;      // will match index i in mem[i]
    uint32_t *data;   // an array of uint32_t
    size_t num_words; // num of uint32_t items
} DynamicArray;

int alloc_array(uint32_t id,  size_t num_words);
uint32_t *construct_instructions(const uint8_t *buffer, int file_size);
void decode_instruction(const uint32_t inst);
void disassemble(const char *filename, const uint32_t *inst_arr,
                 size_t filesize, int disassemble_num);
void op_add();
void op_alloc();
void op_array_index();
void op_array_update();
void op_cond_move();
void op_dealloc();
void op_div();
void op_input();
void op_load_immed();
uint32_t * op_load_prog(uint32_t *prog_ptr);
void op_mult();
void op_nand();
void op_output();
void print_binary(uint32_t x);
uint8_t *read_bin(const char *filename, size_t *filesize);
void run_program(uint32_t *prog_arr, size_t *arr_size);

#endif // EMULATOR_H
