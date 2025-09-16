#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>

uint32_t factorial(int n) {
    if (n < 0) {
        printf("WARNING: factorial(n) called with n < 0.");
        return 0;
    } else if (n == 0 || n == 1) {
        return 1;
    }

    uint32_t temp_prod = 1;
    for (int i = 2; i <= n; i++)
    {
        temp_prod *= i;
    }

    return temp_prod;
}

typedef struct DynamicArray {
    uint32_t id;      // identifier
    uint32_t *data;   // an array of uint32_t
    size_t num_words; // num of uint32_t items
} DynamicArray;

DynamicArray mem;

/**
 * @brief Dynamically create new array of uint32_ts inside DynamicArray
 * @param num_words Desired length of dynamic array in uint32_ts.
 * @return int 1 is successful
*/
// DynamicArray *alloc_array(uint32_t id,  size_t num_words) {
int alloc_array(uint32_t id,  size_t num_words) {

    mem.id = id;
    mem.num_words = num_words;
    mem.data = (uint32_t *)calloc(num_words, sizeof(uint32_t));
    if (mem.data == NULL) {
        printf("WARNING: array allocation failed!\n");
    }

    return 1;
}

int dealloc_array() {
    // id is actually irrelevant
    if (mem.data == NULL) {
        return 0;
    }
    free(mem.data);
    return 0;
}

int main()
{
    const uint32_t num_times = 100000000;
    srand(time(NULL));
    printf("\nAllocating & Deallocating Dynamic Arrays of uint32_t "
           "(%u times).\n\n", num_times);

    clock_t start_time, end_time;
    double time_spent;
    start_time = clock();

    for (int i = 0; i < num_times; i++)
    {
        // Generate a random integer id from min to max
        int min = 1;
        int max = 100;
        int random_id = (rand() % (max - min + 1)) + min;

        // Choose random num_words from min to max
        min = 10;
        max = 20;
        int random_num_words = (rand() % (max - min + 1)) + min;

        alloc_array(random_id, random_num_words);
        dealloc_array();
    }
    
    // compute and report program runtime
    end_time = clock();

    printf("\nArray allocations/deallocations done!\n\n");

    time_spent = (double)(end_time - start_time)/CLOCKS_PER_SEC;
    printf("\nRUN TIME = %.3e secs\n\n", time_spent);
    

    return EXIT_SUCCESS;
}
