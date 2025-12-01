/**
 * filename: examples/compiled/example1-factorial_ast.c
 * created:  2025-12-01
 * descr:    C program produced from the AST of
 *           examples/example1-factorial.while.
*/

#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {

    // Check if correct num of args provided
    if (argc != 5 ){
        printf("Executable requires 4 integer arguments.\n");
        printf("Usage: <filename> output x y z\n");
        return EXIT_FAILURE;
    }

    // Establish array to store the 4 int values
    int var_values[4];

    // Store the user-supplied initial values.
    for (int i = 0; i < 4; i++) {
        var_values[i] = atoi(argv[i + 1]);
    }

    // Declare & initialize the variables.
    int output = var_values[0];
    int x = var_values[1];
    int y = var_values[2];
    int z = var_values[3];

    printf("\nInitial variable values are:\n");

    // Print initialized variable values to verify:
    printf("\n");
    printf("output = %d \n", var_values[0]);
    printf("x = %d \n", var_values[1]);
    printf("y = %d \n", var_values[2]);
    printf("z = %d \n", var_values[3]);

    y = x;
    z = 1;
    while (y > 1) {
        z = z * y;
        y = y - 1;
    }
    y = 0;
    output = z;

    // Print final array values:
    printf("\nFinal variable values are: \n");
    printf("\n");
    printf("output = %d \n", output);
    printf("x = %d \n", x);
    printf("y = %d \n", y);
    printf("z = %d \n", z);

    printf("\n");

    return EXIT_SUCCESS;

}