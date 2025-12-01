/**
 * filename: examples/compiled/primescounter_ast.c
 * created:  2025-12-01
 * descr:    C program produced from the AST of
 *           examples/primescounter.while.
*/

#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {

    // Check if correct num of args provided
    if (argc != 7 ){
        printf("Executable requires 6 integer arguments.\n");
        printf("Usage: <filename> count i k output range result\n");
        return EXIT_FAILURE;
    }

    // Establish array to store the 6 int values
    int var_values[6];

    // Store the user-supplied initial values.
    for (int i = 0; i < 6; i++) {
        var_values[i] = atoi(argv[i + 1]);
    }

    // Declare & initialize the variables.
    int count = var_values[0];
    int i = var_values[1];
    int k = var_values[2];
    int output = var_values[3];
    int range = var_values[4];
    int result = var_values[5];

    printf("\nInitial variable values are:\n");

    // Print initialized variable values to verify:
    printf("\n");
    printf("count = %d \n", var_values[0]);
    printf("i = %d \n", var_values[1]);
    printf("k = %d \n", var_values[2]);
    printf("output = %d \n", var_values[3]);
    printf("range = %d \n", var_values[4]);
    printf("result = %d \n", var_values[5]);

    result = 0;
    while (range >= 2) {
        count = 0;
        i = 2;
        while (i * i <= range) {
            k = range;
            if (count > 0) {
            } else {
                while (k >= 1) {
                    if (k * i == range) {
                        count = count + 1;
                    }
                    k = k - 1;
                }
            }
            i = i + 1;
        }
        if (count > 0) {
        } else {
            result = 1 + result;
        }
        range = range - 1;
    }
    output = result;

    // Print final array values:
    printf("\nFinal variable values are: \n");
    printf("\n");
    printf("count = %d \n", count);
    printf("i = %d \n", i);
    printf("k = %d \n", k);
    printf("output = %d \n", output);
    printf("range = %d \n", range);
    printf("result = %d \n", result);

    printf("\n");

    return EXIT_SUCCESS;

}