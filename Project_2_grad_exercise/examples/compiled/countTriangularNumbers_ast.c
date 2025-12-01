/**
 * filename: examples/compiled/countTriangularNumbers_ast.c
 * created:  2025-12-01
 * descr:    C program produced from the AST of
 *           examples/countTriangularNumbers.while.
*/

#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {

    // Check if correct num of args provided
    if (argc != 8 ){
        printf("Executable requires 7 integer arguments.\n");
        printf("Usage: <filename> count goUpToNumber i isNumFact n output sum\n");
        return EXIT_FAILURE;
    }

    // Establish array to store the 7 int values
    int var_values[7];

    // Store the user-supplied initial values.
    for (int i = 0; i < 7; i++) {
        var_values[i] = atoi(argv[i + 1]);
    }

    // Declare & initialize the variables.
    int count = var_values[0];
    int goUpToNumber = var_values[1];
    int i = var_values[2];
    int isNumFact = var_values[3];
    int n = var_values[4];
    int output = var_values[5];
    int sum = var_values[6];

    printf("\nInitial variable values are:\n");

    // Print initialized variable values to verify:
    printf("\n");
    printf("count = %d \n", var_values[0]);
    printf("goUpToNumber = %d \n", var_values[1]);
    printf("i = %d \n", var_values[2]);
    printf("isNumFact = %d \n", var_values[3]);
    printf("n = %d \n", var_values[4]);
    printf("output = %d \n", var_values[5]);
    printf("sum = %d \n", var_values[6]);

    isNumFact = 0;
    sum = 0;
    n = 1;
    count = 0;
    while (i < goUpToNumber) {
        while (sum <= i) {
            sum = sum + n;
            if (sum == i) {
                isNumFact = 1;
                sum = i + 1;
            }
            n = n + 1;
        }
        if (isNumFact == 1) {
            count = count + 1;
        }
        isNumFact = 0;
        sum = 0;
        n = 1;
        i = i + 1;
    }
    output = count;

    // Print final array values:
    printf("\nFinal variable values are: \n");
    printf("\n");
    printf("count = %d \n", count);
    printf("goUpToNumber = %d \n", goUpToNumber);
    printf("i = %d \n", i);
    printf("isNumFact = %d \n", isNumFact);
    printf("n = %d \n", n);
    printf("output = %d \n", output);
    printf("sum = %d \n", sum);

    printf("\n");

    return EXIT_SUCCESS;

}