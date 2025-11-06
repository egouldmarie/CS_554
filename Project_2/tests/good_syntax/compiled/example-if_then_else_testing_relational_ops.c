#include <stdio.h>
#include <stdlib.h>

extern void example_if_then_else_testing_relational_ops(int64_t *var_arr);

int main(int argc, char *argv[]) {

    // Check if correct num of args provided
    if(argc != 5) {
        printf("Executable requires 4 arguments.\n");
        printf("Usage: <filename> input output x y\n");
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
    printf("input = %lld \n", (long long)var_array[0]);
    printf("output = %lld \n", (long long)var_array[1]);
    printf("x = %lld \n", (long long)var_array[2]);
    printf("y = %lld \n", (long long)var_array[3]);

    example_if_then_else_testing_relational_ops(var_array);

    // Print final array values:
    printf("\nFinal variable values are: \n");
    printf("input = %lld \n", (long long)var_array[0]);
    printf("output = %lld \n", (long long)var_array[1]);
    printf("x = %lld \n", (long long)var_array[2]);
    printf("y = %lld \n", (long long)var_array[3]);
    printf("\n");

    return EXIT_SUCCESS;
}
