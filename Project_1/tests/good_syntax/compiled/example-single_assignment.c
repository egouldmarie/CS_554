#include <stdio.h>
#include <stdlib.h>

extern void example_single_assignment(int64_t *var_arr);

int main(int argc, char *argv[]) {

    // Check if correct num of args provided
    if(argc != 2) {
        printf("Executable requires 1 arguments.\n");
        printf("Usage: <filename> x\n");
        return EXIT_FAILURE;
    }

    // Establish array to store the 1 int values
    int64_t var_array[1];

    // Initialize the values
    for (int i = 0; i < 1; i++) {
        var_array[i] = atoll(argv[i + 1]);
    }

    // Print initialized array values to verify:
    printf("\n");
    printf("Initial variable values are: \n");
    printf("x = %lld \n", (long long)var_array[0]);

    example_single_assignment(var_array);

    // Print final array values:
    printf("\nFinal variable values are: \n");
    printf("x = %lld \n", (long long)var_array[0]);
    printf("\n");

    return EXIT_SUCCESS;
}
