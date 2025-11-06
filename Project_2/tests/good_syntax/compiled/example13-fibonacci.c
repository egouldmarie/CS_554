#include <stdio.h>
#include <stdlib.h>

extern void example13_fibonacci(int64_t *var_arr);

int main(int argc, char *argv[]) {

    // Check if correct num of args provided
    if(argc != 7) {
        printf("Executable requires 6 arguments.\n");
        printf("Usage: <filename> a b n output t z\n");
        return EXIT_FAILURE;
    }

    // Establish array to store the 6 int values
    int64_t var_array[6];

    // Initialize the values
    for (int i = 0; i < 6; i++) {
        var_array[i] = atoll(argv[i + 1]);
    }

    // Print initialized array values to verify:
    printf("\n");
    printf("Initial variable values are: \n");
    printf("a = %lld \n", (long long)var_array[0]);
    printf("b = %lld \n", (long long)var_array[1]);
    printf("n = %lld \n", (long long)var_array[2]);
    printf("output = %lld \n", (long long)var_array[3]);
    printf("t = %lld \n", (long long)var_array[4]);
    printf("z = %lld \n", (long long)var_array[5]);

    example13_fibonacci(var_array);

    // Print final array values:
    printf("\nFinal variable values are: \n");
    printf("a = %lld \n", (long long)var_array[0]);
    printf("b = %lld \n", (long long)var_array[1]);
    printf("n = %lld \n", (long long)var_array[2]);
    printf("output = %lld \n", (long long)var_array[3]);
    printf("t = %lld \n", (long long)var_array[4]);
    printf("z = %lld \n", (long long)var_array[5]);
    printf("\n");

    return EXIT_SUCCESS;
}
