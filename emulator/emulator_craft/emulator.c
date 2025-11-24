#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>
#include <stdbool.h>
#include <string.h>
#include <math.h>

#include "emulator.h"
// #include "uint32_stack.h"

/* ============================================= */
/*   Global utility structures.                  */
/* ============================================= */

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

/* 8 general-purpose 32-bit registers */
uint32_t reg[8] = {0};

/* A pseudo-stack for storing available uint32_t IDs */
struct StackNode* avail_ids = NULL;

// A 5-int array to hold the OpCode, A, B, C, value
// for a parsed instruction.
uint32_t decoded_instruction[5];

// struct to hold dynamic array info, which should
// then should allow us to produce an array of such
// dynamic arrays. This now appears in the header file.
// typedef struct {
//     uint32_t id;      // will match index i in mem[i]
//     uint32_t *data;   // an array of uint32_t
//     size_t num_words; // num of uint32_t items
// } DynamicArray;

DynamicArray *mem = NULL; // might need: uint32_t ** mem = NULL
// uint32_t ** mem = NULL;
size_t arr_count  = 0;

/* ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ */
/*   END of Global utility structures.           */
/* ============================================= */

int min(int a, int b) {
    return (a < b) ? a : b;
}

/**
 * @brief Dynamically create new DynamicArray and add to mem[] array
 * @param num_words Desired length of DynamicArray.
 * @return Ptr to the new DynamicArray.
*/
// DynamicArray *alloc_array(uint32_t id,  size_t num_words) {
int alloc_array(uint32_t id,  size_t num_words) {

    // only RE-alloc if we need a new pointer and can't use a previous
    // one that has been deallocated.
    if (id == arr_count) {
        // need to expand current array of pointers to DynamicArrays
        arr_count++;
        mem = (DynamicArray *)realloc(mem, arr_count * sizeof(DynamicArray));
        if (mem == NULL) {
            perror("realloc failed in alloc_array()");
            return 0;
        }
    } // else we should be able to re-use the id w/out expanding
      // the array of ptrs

    // At this point mem[id] should have memory allocated.

    mem[id].id = id;
    mem[id].num_words = num_words;
    mem[id].data = (uint32_t *)calloc(num_words, sizeof(uint32_t));

    // consider an error check:
    // if (mem[id]->data == NULL) {
    //     free(mem[id]->data);
    //     free(mem[id]);
    //     return 0; // calling function should check
    // }

    return 1;
}

/**
 * @brief Print the binary expansion of an unsigned 32-bit int.
 * @param x An unsigned 32 bit int of type uint32_t.
 * @return void.
*/
void print_binary(uint32_t x) {
    for(int i = 31; i >= 0; i--) {
        printf("%d", (x >> i) & 1);
    }
}

/**
 * @brief Construct and return array of 32-bit instructions.
 * @param buffer An array of hexadecimal program instructions.
 * @param file_size The # bytes of buffer array.
 * @return instruction_array The array of 32-bit instructions.
*/
uint32_t *construct_instructions(const uint8_t *buffer, int file_size) {

    uint32_t *instruction_array = (uint32_t *)malloc(file_size);

    for (int i = 0; i < file_size; i = i+4) {
        uint32_t combined_binary = 0;
        combined_binary |= (uint32_t)buffer[i]   << 24;
        combined_binary |= (uint32_t)buffer[i+1] << 16;
        combined_binary |= (uint32_t)buffer[i+2] <<  8;
        combined_binary |= (uint32_t)buffer[i+3];
        instruction_array[i/4] = combined_binary;
    }

    return instruction_array;
}

/**
 * @brief Read in binary program file.
 * @param filename Ptr to the program filename.
 * @param filesize Ptr to the filesize (content to be set by fxn).
 * @return instruction_array The array of 32-bit instructions.
 * 
 * We read the binary hexadecimal file one byte at a time, instead
 * of trying to capture 4 bytes at a time, to avoid endian issues. 
 * For example, the program files are written in big-endian ABCD
 * so that A is the most significant byte, but some sytems (such as
 * my MacOS) interpret the input as little endian, effectively
 * producing DCBA as the result if read as 4 bytes. We read the data
 * into an array of bytes, then construct each word manually (in a
 * separate function) from the 4-byte sequences.
 * The filesize ptr supplied as an argument is used by the function
 * to "return" the filesize --- i.e., calling the function does not
 * require the filesize to be known ahead of time.
*/
uint8_t *read_bin(const char *filename, size_t *filesize) {

    FILE *file = fopen(filename, "rb");
    if (file == NULL) {
        perror("Error opening file!");
        return NULL;
    }

    long file_size;
    uint8_t *buffer;

    // determine file size
    fseek(file, 0, SEEK_END);
    file_size = ftell(file);
    rewind(file);

    *filesize = file_size;

    // allocate memory for the buffer
    buffer = (uint8_t *)malloc(file_size);
    if (buffer == NULL) {
        perror("Error allocating memory for buffer!");
        fclose(file);
        return NULL;
    }

    // read file into buffer, 1 byte (2 hex chars) at a time
    size_t bytes_read = fread(buffer, 1, file_size, file);
    if (bytes_read != file_size) {
        fprintf(stderr,
            "Error reading file: Expected %ld bytes, but read %zu bytes.\n",
            file_size, bytes_read);
        free(buffer);
        fclose(file);
        return NULL;
    }

    // close the file
    fclose(file);

    return buffer;
}

/**
 * @brief Disassemble & print summary of array of 32-bit instructions.
 * @param filename Ptr to the original program filename.
 * @param filesize Size of original program file.
 * @return void.
*/
void disassemble(const char *filename, const uint32_t *inst_arr,
                 size_t filesize, int disassemble_num) {

    int num_instrs = filesize/sizeof(uint32_t);
    int num_lines = disassemble_num == -1? num_instrs : disassemble_num;
    num_lines = min(num_lines, num_instrs);

    // Disassemble & Summarize the 32-bit program instructions 
    printf("PROGRAM INSTRUCTIONS DIS-ASSEMBLY & SUMMARY\n");
    printf("FILE: %s\n", filename);
    printf("FILE SIZE (bytes): %zu\n", filesize);
    printf("Number of 32-bit 'instruction' words: %d\n", num_instrs);
    printf("Note: Opcodes > 13 are invalid and are indicated by --.\n");
    printf("Note: 'value' reported only for OpCodes >= 13.\n\n");
    printf("Instruction                       Opcode   A     B     C  "
           "  value\n");
    printf("=========================================================="
           "============\n");
    for (int i  = 0; i < num_lines; i++) {
        uint32_t temp_binary = inst_arr[i];
        // print the instruction in binary
        print_binary(temp_binary);
        // the following updates global int array 'decoded_instruction'
        decode_instruction(temp_binary);
        // Opcode
        uint32_t opcode = decoded_instruction[0];
        // printf("   %3d", opcode);
        if (opcode <= 13) {
            printf("   %3u", opcode);
        } else {
            printf("    --");
        }

        // Reg A
        if (opcode <= 13) {
            printf("   %3u", decoded_instruction[1]);
        } else {
            printf("    --");
        }
        // Reg B
        if (opcode < 13) {
            printf("   %3u", decoded_instruction[2]);
        } else {
            printf("    --");
        }
        // Reg C
        if (opcode < 13) {
            printf("   %3u", decoded_instruction[3]);
        } else {
            printf("    --");
        }
        // Value for Opcode 13
        if (opcode >= 13) {
            printf("      %4u", decoded_instruction[4]);
        }
        printf("\n");
    }
    
    printf("\n");
    printf("==== END OF SUMMARY ===");
    printf("\n\n");

}

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

/**
 * @brief Parse a 32-bit instruction into components.
 * @param inst A 32-bit instruction.
 * @return void. Stores result in caller-provided array 'decoded'.
*/
void local_decode_instruction(const uint32_t inst, uint32_t *decoded) {
    // A localized-output version of the decode_instruction() fxn,
    // used as a helper function in debugging.

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

    decoded[0] = opcode;
    decoded[1] = a;
    decoded[2] = b;
    decoded[3] = c;
    decoded[4] = value;
}

// =============================================== //
//      OpCode OPERATIONS                          //
//      (numerical order by OpCode)                //
// =============================================== //

/* Note that decoded_inst_arr has the format:
   {opcode, a, b, c, value}                        */

// OpCode 0 COND_MOVE
void op_cond_move() {
    // If reg[c] is not 0, reg[a] := reg[b]

    uint32_t a, b, c;
    a = decoded_instruction[1];
    b = decoded_instruction[2];
    c = decoded_instruction[3];

    if (reg[c] != 0) {
        reg[a] = reg[b];
    }
}

// OpCode 1 ARRAY_INDEX
void op_array_index() {
    // reg[a] receives value stored at offset in reg[c] in
    // array mem[reg[b]].

    uint32_t a, b, c;
    a = decoded_instruction[1];
    b = decoded_instruction[2];
    c = decoded_instruction[3];

    reg[a] = mem[reg[b]].data[reg[c]];
}

// OpCode 2 ARRAY_UPDATE
void op_array_update() {
    // Array identified by reg[a] is updated at the offset in
    // reg[b] to store the value in reg[c]

    uint32_t a, b, c;
    a = decoded_instruction[1];
    b = decoded_instruction[2];
    c = decoded_instruction[3];

    mem[reg[a]].data[reg[b]] = reg[c];
}

// OpCode 3 ADD
void op_add() {
    // reg[a] := (reg[b] + reg[c]) % 2^{32}
    // explict % should not be necessary using uint32_t
    uint32_t a = decoded_instruction[1];
    uint32_t b = decoded_instruction[2];
    uint32_t c = decoded_instruction[3];
    reg[a] = reg[b] + reg[c];
}

// OpCode 4 MULT
void op_mult() {
    // reg[a] := (reg[b] * reg[c]) % 2^{32}
    // explict % should not be necessary using uint32_t
    uint32_t a = decoded_instruction[1];
    uint32_t b = decoded_instruction[2];
    uint32_t c = decoded_instruction[3];
    reg[a] = reg[b] * reg[c];
}

// OpCode 5 DIV
void op_div() {
    // reg[a] := (reg[b] / reg[c]) % 2^{32}
    // explict % should not be necessary using uint32_t
    // Integer division.
    uint32_t a = decoded_instruction[1];
    uint32_t b = decoded_instruction[2];
    uint32_t c = decoded_instruction[3];
    reg[a] = reg[b] / reg[c];
}

// OpCode 6 NAND
void op_nand() {
    // reg[a] := (reg[b] NAND reg[c])
    // x NAND y = ~ (x AND y)
    uint32_t a = decoded_instruction[1];
    uint32_t b = decoded_instruction[2];
    uint32_t c = decoded_instruction[3];
    
    reg[a] = ~ (reg[b] & reg[c]);
}

// OpCode 7 HALT
// no explicit operation, with HALT being the default for
// ending the program by not entering the while() loop

// OpCode 8 ALLOC
void op_alloc() {
    // allocate a new array of 32-bit words
    uint32_t b = decoded_instruction[2];
    uint32_t c = decoded_instruction[3];

    // generate a new uint32_t id or
    // reuse a discarded id for the new array
    uint32_t id;
    if (!isEmpty(avail_ids)) {
        id = pop(&avail_ids);
    } else {
        id = arr_count;
    }
    if (id == (uint32_t)0) {
        printf("WARNING: Using array id = 0.");
    }

    alloc_array(id, reg[c]);

    reg[b] = id;
}

// OpCode 9 DEALLOC
void op_dealloc() {
    // Array identified by register c is deallocated.
    // Future allocations may reuse the identifier.

    uint32_t c = decoded_instruction[3];
    uint32_t id = reg[c];

    if (mem[id].data != NULL) {
        free(mem[id].data);
        mem[id].data = NULL; // Good practice make NULL after free()
        push(&avail_ids, id);
    }

}

// OpCode 10 OUTPUT
void op_output() {
    printf("%c", reg[decoded_instruction[3]]);
}

// OpCode 11 INPUT
void op_input() {
    // Each key press is captured and put into reg[c].
    // The program itself generally provides no textual prompt and
    // because of its design, trying to provide a prompt for the
    // user here in the emulator just gets in the way. This approach
    // also makes it difficult to provide any input error checking
    // during runtime. Expected behavior is user can keep entering
    // appropriate digits until a hard return, at which point the
    // program has accumulated the digits and proceeds with processing.
    // The "end of input" signal is processed by the program instead
    // of being explicitly processed here in the emulator.
    // Ultimately we might want to seek further control over the
    // timing here so the time does not included user response time.

    uint32_t c = decoded_instruction[3];

    // this worked! but so does the variation further below
    // char first_byte;
    // size_t bytes_read = fread(&first_byte, 1, 1, stdin);
    // reg[c] = first_byte;

    int ch;
    ch = getc(stdin);
    reg[c] = ch;
    
}

// OpCode 12 LOAD_PROG
uint32_t * op_load_prog(uint32_t *prog_ptr) {
    // Array id'd by register B is duplicated, and the duplicate
    // replaces the zero_arr, regardless of size.
    // If we try to do this by just changing where the mem[0].data
    // pointer points (instead of duplicating), we could run into
    // trouble if the program later then attempts to manipulate the
    // the array we should have duplicated.
    // Notice that if the array to be duplicated is in fact the
    // zero array, we ignore the duplication request and simply
    // update the program counter pc.
    // Notice also that it makes no sense to duplicate an array
    // that doesn't already exist, so a future error-check should
    // include a quick check for that to help with debugging issues.
    
    uint32_t b = decoded_instruction[2];
    uint32_t c = decoded_instruction[3];
    uint32_t offset = reg[c];

    if (reg[b] != 0) {

        // Allocate memory for a COPY of the array identified by
        // the B register --- i.e. copy of mem[reb[b]].data
        size_t new_arr_size = mem[reg[b]].num_words * sizeof(uint32_t);
        uint32_t *new_arr = (uint32_t *)malloc(new_arr_size);
        if (new_arr == NULL) {
            perror("Failed to allocate memory for new array.");
            return NULL; // memory allocation failure
        }

        // Copy elements from original array into new array
        memcpy(new_arr, mem[reg[b]].data, new_arr_size);

        // Then point mem[0].data pointer to the new array, first
        // freeing up the memory (if any) to which it already points.
        if (mem[0].data != NULL) {
            free(mem[0].data);
            mem[0].data = NULL;
        }
        mem[0].data = new_arr;
    }
    
    // update program counter regardless of whether or not
    // a brand new array was swapped in for the zero array
    prog_ptr = mem[0].data + offset;
    return prog_ptr;
}

// OpCode 13 LOAD_IMMED
void op_load_immed() {
    // printf("    Entering op_load_immed() fxn.\n");
    reg[decoded_instruction[1]] = decoded_instruction[4];
    // printf("    Finished op_load_immed() fxn.\n");

}

// ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ //
//      END of OpCode OPERATIONS                   //
// ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ //

void run_program(uint32_t *prog_arr, size_t *arr_size) {

    // could re-call run_program from the op_load() function
    // but could also realize that prog_arr is simply mem[0]
    // so resetting mem[0] ... 

    // consider removing the prog_arr arg and just using the
    // global mem[0]

    uint32_t *pc;
    pc = prog_arr;
    // long unsigned num_instrs = *arr_size / sizeof(prog_arr[0]);
    bool unexpected_halt = false;
    bool illegitimate_code_found = false;
    uint32_t illegitimate_code;
    
    // printf("\n\n=====   RUNNING PROGRAM   =====\n\n");

    // printf("Program arr_size = %zu bytes.\n", *arr_size);
    // printf("Size of array elem = %zu bytes.\n", sizeof(prog_arr[0]));
    // printf("Thus, number of array elems = %lu\n\n", num_instrs);
    
    // get 1st instruction info
    decode_instruction(*pc);
    uint32_t opcode = decoded_instruction[0];

    while (opcode != HALT) {

        switch (opcode) {

            case COND_MOVE: // 0
                op_cond_move();
                break;
            
            case ARR_INDEX: // 1
                op_array_index();
                break;

            case ARR_UPDATE: // 2
                op_array_update();
                break;
            
            case ADD: // 3
                op_add();
                break;
            
            case MULT: // 4
                op_mult();
                break;
            
            case DIV: // 5
                op_div();
                break;
            
            case NAND: // 6
                op_nand();
                break;

            case ALLOC: // 8
                op_alloc();
                break;
            
            case DEALLOC: // 8
                op_dealloc();
                break;

            case OUTPUT: // 10
                op_output();
                break;
            
            case INPUT: // 11
                op_input();
                break;
            
            case LOAD_PROG: // 12
                pc = op_load_prog(pc);
                pc--;
                break;
            
            case LOAD_IMMED: // 13
                op_load_immed();
                break;
            
            default:
                illegitimate_code_found = true;
                illegitimate_code = opcode;
                opcode = 7;
                
                break;
        }

        // We proceed without error checking, letting invalid codes
        // get caught in the default switch case and ending program.
        decode_instruction(*(++pc));
        opcode = decoded_instruction[0];
        
    }

    if (unexpected_halt) {
        printf("WARNING: Program instructions ended unexpectedly.\n");
    }
    if (illegitimate_code_found){
        printf("WARNING: Encountered Illegitimate OpCode: %u\n",
              illegitimate_code);
    }
}

int main(int argc, char *argv[])
{
    /* Filename, Flags, and Default Settings */
    char *filename = NULL;
    // -d flag prompts disassembly summary output
    bool disassemble_flag = false;
    int  disassemble_num  = -1;

    // Check if a filename argument was provided
    if (argc < 2) {
        printf("\nUsage: %s <filename>\n\n", argv[0]);
        return EXIT_FAILURE; // Exit with an error code
    }

    // Iterate through arguments to find filename and flags
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "-d") == 0) {
            disassemble_flag = true;
            if (i + 1 < argc) {
                disassemble_num = atoi(argv[i+1]);
                i++; // skip next arg as it's the value
            } else {
                printf("WARNING: Flag -d requires a value.\n");
                return EXIT_FAILURE;
            }
        } else {
            // Assume 1st non-flag arg is filename
            if (filename == NULL) {
                filename = argv[i];
            } else {
                printf("\nWARNING: Multiple filenames or unknown "
                       "flags provided.\n\n");
                return EXIT_FAILURE;
            }
        }
    }
    
    // char *filename = argv[1];
    printf("\nReading hexadecimal values from program file: %s\n\n",
           filename);

    size_t filesize;

    // Read in the raw program file of hexadecimal characters
    // char *raw_file_data = read_bin(filename, &filesize);
    u_int8_t *raw_file_data = read_bin(filename, &filesize);

    // Explicitly construct the array of 32-bit program instruction
    // words and store the resulting array of 32-bit words in the
    // "zero array"

    alloc_array(0,  filesize/4);
    mem[0].data = construct_instructions(raw_file_data, filesize);

    // int temp_len = min( mem[0].num_words, 10 );
    // printf("\n\n================================\n");
    // for (int i = 0; i < temp_len; i++) {
    //     print_binary((mem[0].data)[i]);
    //     printf("\n");
    // }
    // printf("================================\n\n");

    if (disassemble_flag) {
        disassemble(filename, mem[0].data, filesize, disassemble_num);
    }

    printf("\n=====   RUNNING PROGRAM   =====\n\n");

    // Run program, wrapped in a timer setup
    clock_t start_time, end_time;
    double time_spent;
    start_time = clock();

    run_program(mem[0].data, &filesize);

    // compute and report program runtime
    end_time = clock();

    printf("\n===== END RUNNING PROGRAM =====\n");

    time_spent = (double)(end_time - start_time)/CLOCKS_PER_SEC;
    printf("\nRUN TIME = %.2e secs\n\n", time_spent);

    /* Free the manually-allocated memory. Technically not
       required if program ending (i.e., OS should handle OK),
       but recommended as good practice.
    */
    free(raw_file_data);
    free(mem[0].data);
    free(&(mem[0]));

    return EXIT_SUCCESS;
}
