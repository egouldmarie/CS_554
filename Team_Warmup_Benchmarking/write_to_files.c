#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main()
{
    FILE *fPtr;

    for (int i = 0; i < 10000; ++i)
    {
        char filename[20];
        sprintf(filename, "test/file%d.txt", i);
        if (access(filename, F_OK) == 0)
        {
            fPtr = fopen(filename, "w");

            if (fPtr == NULL)
            {
                exit(EXIT_FAILURE);
            }

            char data[1000] = {0};
            fputs(data, fPtr);
            fclose(fPtr);
        }
        else
        {
            exit(EXIT_FAILURE);
        }
    }

    return 0;
}