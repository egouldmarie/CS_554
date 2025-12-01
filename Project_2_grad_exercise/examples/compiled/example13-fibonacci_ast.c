/**
 * filename: examples/compiled/example13-fibonacci_ast.c
 * created:  2025-12-01
 * descr:    C program produced from the AST of
 *           examples/example13-fibonacci.while.
*/

#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {

    // Check if correct num of args provided
    if (argc != 7 ){
        printf("Executable requires 6 integer arguments.\n");
        printf("Usage: <filename> a b n output t z\n");
        return EXIT_FAILURE;
    }

    // Establish array to store the 6 int values
    int var_values[6];

    // Store the user-supplied initial values.
    for (int i = 0; i < 6; i++) {
        var_values[i] = atoi(argv[i + 1]);
    }

    // Declare & initialize the variables.
    int a = var_values[0];
    int b = var_values[1];
    int n = var_values[2];
    int output = var_values[3];
    int t = var_values[4];
    int z = var_values[5];

    printf("\nInitial variable values are:\n");

    // Print initialized variable values to verify:
    printf("\n");
    printf("a = %d \n", var_values[0]);
    printf("b = %d \n", var_values[1]);
    printf("n = %d \n", var_values[2]);
    printf("output = %d \n", var_values[3]);
    printf("t = %d \n", var_values[4]);
    printf("z = %d \n", var_values[5]);

    a = 0;
    b = 1;
    z = 0;
    while (!(n == z)) {
        t = a + b;
        a = b;
        b = t;
        n = n - 1;
        z = 0;
    }
    output = a;

    // Print final array values:
    printf("\nFinal variable values are: \n");
    printf("\n");
    printf("a = %d \n", a);
    printf("b = %d \n", b);
    printf("n = %d \n", n);
    printf("output = %d \n", output);
    printf("t = %d \n", t);
    printf("z = %d \n", z);

    printf("\n");

    return EXIT_SUCCESS;

}