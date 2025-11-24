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

int main()
{
    const uint32_t num_times = 100000000;

    printf("\nCalculating n! for n = 1, 2, ..., 12 ... "
           "(%u times).\n\n", num_times);

    // for (int i = 0; i < 13; i++)
    // {
    //     printf("%2d! = %d\n", i, factorial(i));
    // }

    clock_t start_time, end_time;
    double time_spent;
    start_time = clock();

    uint32_t result = 0;

    for (int i = 0; i < num_times; i++)
    {
        for (int i = 0; i < 13; i++)
        {
            result = factorial(i);
        }
    }

    // compute and report program runtime
    end_time = clock();

    printf("\nCalculations done!\n\n");

    time_spent = (double)(end_time - start_time)/CLOCKS_PER_SEC;
    printf("\nRUN TIME = %.2e secs\n\n", time_spent);
    

    return EXIT_SUCCESS;
}
