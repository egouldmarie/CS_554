#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>


int main(int argc, char *argv[])
{
    /* Filename, Flags, and Default Settings */
    char *filename = NULL;
    int  disassemble_num  = -1;
    int num_vars = 4;
    char *printVars = "output x y x";
    char *var_names[] = {"output", "x", "y", "z"};

    // Check if a filename argument was provided
    if (argc < 2) {
        printf("\nUsage: %s <filename>\n\n", argv[0]);
        return EXIT_FAILURE; // Exit with an error code
    }

    // Check if correct num of args provided
    if (argc != 5) {
        printf("Executable requires %d arguments.\n", num_vars);
        printf("Usage: <filename> %s\\n", printVars);
        return EXIT_FAILURE;
    }

    int64_t output, x, y, z;

    x = 0;
    y = 0;
    z = 0;

    y = x;
    z = 1;

    while (y > 1) {
        z = z * y;
        y = y - 1;
    }
    y = 0;
    output = z;

    return EXIT_SUCCESS;
}