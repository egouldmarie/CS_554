/**
 * filename: examples/compiled/example6-collatz_cfg.c
 * created:  2025-12-01
 * descr:    C program produced from the CFG of
 *           examples/example6-collatz.while.
*/

#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {

    // Check if correct num of args provided
    if (argc != 7 ){
        printf("Executable requires 6 integer arguments.\n");
        printf("Usage: <filename> input n output quot rem steps\n");
        return EXIT_FAILURE;
    }

    // Establish array to store the 6 int values
    int var_values[6];

    // Store the user-supplied initial values.
    for (int i = 0; i < 6; i++) {
        var_values[i] = atoi(argv[i + 1]);
    }

    // Declare & initialize the variables.
    int input = var_values[0];
    int n = var_values[1];
    int output = var_values[2];
    int quot = var_values[3];
    int rem = var_values[4];
    int steps = var_values[5];

    printf("\nInitial variable values are:\n");

    // Print initialized variable values to verify:
    printf("\n");
    printf("input = %d \n", var_values[0]);
    printf("n = %d \n", var_values[1]);
    printf("output = %d \n", var_values[2]);
    printf("quot = %d \n", var_values[3]);
    printf("rem = %d \n", var_values[4]);
    printf("steps = %d \n", var_values[5]);

    n = input;
    steps = 0;
    while (n > 1) {
        rem = n;
        quot = 0;
        while (rem > 1) {
            rem = rem - 2;
            quot = quot + 1;
        }
        if (rem == 0) {
            n = quot;
        } else {
            n = 3 * n + 1;
        }
        steps = steps + 1;
    }
    output = steps;

    // Print final array values:
    printf("\nFinal variable values are: \n");
    printf("\n");
    printf("input = %d \n", input);
    printf("n = %d \n", n);
    printf("output = %d \n", output);
    printf("quot = %d \n", quot);
    printf("rem = %d \n", rem);
    printf("steps = %d \n", steps);

    printf("\n");

    return EXIT_SUCCESS;

}