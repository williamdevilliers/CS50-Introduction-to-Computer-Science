#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Only accepts 2 command-line arguments\n");
        return 1;
    }
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }
    BYTE buffer[512];
    char filename[8];
    int count = 0;
    FILE *pointer = NULL;
    while (fread(&buffer, 512, 1, input))
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff)
        {
            if (!(count == 0))
            {
                fclose(pointer);
            }
            sprintf(filename, "%03i.jpg", count);
            pointer = fopen(filename, "w");
            count++;
        }
        if (!(count == 0))
            {
                fwrite(&buffer, 512, 1, pointer);
            }
    }
    fclose(input);
    fclose(pointer);
    return 0;
    
}