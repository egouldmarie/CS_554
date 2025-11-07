#include <stdio.h>
#include <stdlib.h>

extern void countTriangularNumbers(int64_t *var_arr);

int main(int argc, char *argv[]) {

    // Check if correct num of args provided
    if(argc != 8) {
        printf("Executable requires 7 arguments.\n");
        printf("Usage: <filename> count goUpToNumber i isNumFact n output sum\n");
        return EXIT_FAILURE;
    }

    // Establish array to store the 7 int values
    int64_t var_array[7];

    // Initialize the values
    for (int i = 0; i < 7; i++) {
        var_array[i] = atoll(argv[i + 1]);
    }

    // Print initialized array values to verify:
    printf("\n");
    printf("Initial variable values are: \n");
    printf("count = %lld \n", (long long)var_array[0]);
    printf("goUpToNumber = %lld \n", (long long)var_array[1]);
    printf("i = %lld \n", (long long)var_array[2]);
    printf("isNumFact = %lld \n", (long long)var_array[3]);
    printf("n = %lld \n", (long long)var_array[4]);
    printf("output = %lld \n", (long long)var_array[5]);
    printf("sum = %lld \n", (long long)var_array[6]);

    countTriangularNumbers(var_array);

    // Print final array values:
    printf("\nFinal variable values are: \n");
    printf("count = %lld \n", (long long)var_array[0]);
    printf("goUpToNumber = %lld \n", (long long)var_array[1]);
    printf("i = %lld \n", (long long)var_array[2]);
    printf("isNumFact = %lld \n", (long long)var_array[3]);
    printf("n = %lld \n", (long long)var_array[4]);
    printf("output = %lld \n", (long long)var_array[5]);
    printf("sum = %lld \n", (long long)var_array[6]);
    printf("\n");

    return EXIT_SUCCESS;
}
