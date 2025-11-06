#include <stdio.h>
#include <stdlib.h>

extern void example1_factorial(int64_t *var_arr);

int main(int argc, char *argv[]) {

    // Check if correct num of args provided
    if(argc != 5) {
        printf("Executable requires 4 arguments.\n");
        printf("Usage: <filename> output x y z\n");
        return EXIT_FAILURE;
    }

    // Establish array to store the 4 int values
    int64_t var_array[4];

    // Initialize the values
    for (int i = 0; i < 4; i++) {
        var_array[i] = atoll(argv[i + 1]);
    }

    // Print initialized array values to verify:
    printf("\n");
    printf("Initial variable values are: \n");
    printf("output = %lld \n", (long long)var_array[0]);
    printf("x = %lld \n", (long long)var_array[1]);
    printf("y = %lld \n", (long long)var_array[2]);
    printf("z = %lld \n", (long long)var_array[3]);

    example1_factorial(var_array);

    // Print final array values:
    printf("\nFinal variable values are: \n");
    printf("output = %lld \n", (long long)var_array[0]);
    printf("x = %lld \n", (long long)var_array[1]);
    printf("y = %lld \n", (long long)var_array[2]);
    printf("z = %lld \n", (long long)var_array[3]);
    printf("\n");

    return EXIT_SUCCESS;
}
