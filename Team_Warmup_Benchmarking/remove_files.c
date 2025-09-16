#include <stdio.h>
#include <stdlib.h>

int main()
{
    for (int i = 0; i < 10000; ++i)
    {
        char filename[20];
        sprintf(filename, "test/file%d.txt", i);

        if (remove(filename) != 0)
        {
            exit(EXIT_FAILURE);
        }
    }

    return 0;
}