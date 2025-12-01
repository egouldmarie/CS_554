#include <stdio.h>
#include <stdlib.h>

extern void primescounter(int64_t *var_arr);

int main(int argc, char *argv[]) {

    // Check if correct num of args provided
    if(argc != 7) {
        printf("Executable requires 6 arguments.\n");
        printf("Usage: <filename> count i k output range result\n");
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
    printf("count = %lld \n", (long long)var_array[0]);
    printf("i = %lld \n", (long long)var_array[1]);
    printf("k = %lld \n", (long long)var_array[2]);
    printf("output = %lld \n", (long long)var_array[3]);
    printf("range = %lld \n", (long long)var_array[4]);
    printf("result = %lld \n", (long long)var_array[5]);

    primescounter(var_array);

    // Print final array values:
    printf("\nFinal variable values are: \n");
    printf("count = %lld \n", (long long)var_array[0]);
    printf("i = %lld \n", (long long)var_array[1]);
    printf("k = %lld \n", (long long)var_array[2]);
    printf("output = %lld \n", (long long)var_array[3]);
    printf("range = %lld \n", (long long)var_array[4]);
    printf("result = %lld \n", (long long)var_array[5]);
    printf("\n");

    return EXIT_SUCCESS;
}
