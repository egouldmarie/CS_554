#include <stdio.h>
#include <stdlib.h>

//&Jlqou8^w$w8%sYG

int main()
{
    FILE *fPtr;

    for (int i = 0; i < 10000; ++i)
    {
        char filename[20];
        sprintf(filename, "file%d.txt", i);
        fPtr = fopen(filename, "w");

        if (fPtr == NULL)
        {
            exit(EXIT_FAILURE);
        }

        fclose(fPtr);
    }

    return 0;
}