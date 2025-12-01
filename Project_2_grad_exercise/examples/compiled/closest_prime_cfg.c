/**
 * filename: examples/compiled/closest_prime_cfg.c
 * created:  2025-12-01
 * descr:    C program produced from the CFG of
 *           examples/closest_prime.while.
*/

#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {

    // Check if correct num of args provided
    if (argc != 10 ){
        printf("Executable requires 9 integer arguments.\n");
        printf("Usage: <filename> closestprime i input j mod output sqrt stop stop1\n");
        return EXIT_FAILURE;
    }

    // Establish array to store the 9 int values
    int var_values[9];

    // Store the user-supplied initial values.
    for (int i = 0; i < 9; i++) {
        var_values[i] = atoi(argv[i + 1]);
    }

    // Declare & initialize the variables.
    int closestprime = var_values[0];
    int i = var_values[1];
    int input = var_values[2];
    int j = var_values[3];
    int mod = var_values[4];
    int output = var_values[5];
    int sqrt = var_values[6];
    int stop = var_values[7];
    int stop1 = var_values[8];

    printf("\nInitial variable values are:\n");

    // Print initialized variable values to verify:
    printf("\n");
    printf("closestprime = %d \n", var_values[0]);
    printf("i = %d \n", var_values[1]);
    printf("input = %d \n", var_values[2]);
    printf("j = %d \n", var_values[3]);
    printf("mod = %d \n", var_values[4]);
    printf("output = %d \n", var_values[5]);
    printf("sqrt = %d \n", var_values[6]);
    printf("stop = %d \n", var_values[7]);
    printf("stop1 = %d \n", var_values[8]);

    mod = input;
    while (!(mod == 1 || mod == 0)) {
        mod = mod - 2;
    }
    if (mod == 1) {
        input = input - 2;
    } else {
        input = input - 1;
    }
    i = input;
    stop1 = 0;
    while (i >= 2 && stop1 == 0) {
        sqrt = 1;
        while (sqrt * sqrt <= i) {
            sqrt = sqrt + 1;
        }
        j = 3;
        stop = 0;
        while (j <= sqrt && stop == 0) {
            mod = i;
            while (mod > 0) {
                mod = mod - j;
            }
            if (mod == 0) {
                stop = 1;
            } else {
                j = j + 2;
            }
        }
        if (j > sqrt) {
            stop1 = 1;
        } else {
            i = i - 2;
        }
    }
    closestprime = i;
    output = closestprime;

    // Print final array values:
    printf("\nFinal variable values are: \n");
    printf("\n");
    printf("closestprime = %d \n", closestprime);
    printf("i = %d \n", i);
    printf("input = %d \n", input);
    printf("j = %d \n", j);
    printf("mod = %d \n", mod);
    printf("output = %d \n", output);
    printf("sqrt = %d \n", sqrt);
    printf("stop = %d \n", stop);
    printf("stop1 = %d \n", stop1);

    printf("\n");

    return EXIT_SUCCESS;

}