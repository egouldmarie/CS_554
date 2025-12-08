#include <stdio.h>
#include <stdlib.h>

extern void primescounter(int64_t *var_arr);

int main(int argc, char *argv[]) {

    // Check if correct num of args provided
    if(argc != 2) {
        printf("Executable requires 1 argument(s).\n");
        printf("Usage: <filename> range\n");
        return EXIT_FAILURE;
    }

    // Establish array to store the 6 int values
    int64_t var_array[6];

    // Initialize the values
    var_array[0] = atoll(argv[1]);
    var_array[1] = 0;
    var_array[2] = 0;
    var_array[3] = 0;
    var_array[4] = 0;
    var_array[5] = 0;

    // Print initialized array values to verify:
    printf("\n");
    printf("Initial variable values are: \n");
    printf("range = %lld \n", (long long)var_array[0]);
    printf("count = %lld \n", (long long)var_array[1]);
    printf("i = %lld \n", (long long)var_array[2]);
    printf("k = %lld \n", (long long)var_array[3]);
    printf("output = %lld \n", (long long)var_array[4]);
    printf("result = %lld \n", (long long)var_array[5]);

    primescounter(var_array);

    // Print final array values:
    printf("\nFinal variable values are: \n");
    printf("range = %lld \n", (long long)var_array[0]);
    printf("count = %lld \n", (long long)var_array[1]);
    printf("i = %lld \n", (long long)var_array[2]);
    printf("k = %lld \n", (long long)var_array[3]);
    printf("output = %lld \n", (long long)var_array[4]);
    printf("result = %lld \n", (long long)var_array[5]);
    printf("\n");

    return EXIT_SUCCESS;
}
