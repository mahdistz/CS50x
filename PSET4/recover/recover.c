#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE.\n");
        return 1;
    }

    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file %s.\n", argv[1]);
        return 2;
    }

    unsigned char *temp = malloc(512);
    char *filename = malloc(8);
    int jpeg = 0;

    if (temp == NULL)
    {
        return 1;
    }

    while (fread(temp, sizeof(unsigned char), 512, input))
    {
        if (temp[0] == 0xff && temp[1] == 0xd8 && temp[2] == 0xff && (temp[3] & 0xf0) == 0xe0)
        {
            sprintf(filename, "%03i.jpg", jpeg);
            FILE *output = fopen(filename, "w");
            fwrite(temp, 1, 512, output);
            fclose(output);

            jpeg++;
        }
        else if (jpeg != 0)
        {
            FILE *output = fopen(filename, "a");
            fwrite(temp, 1, 512, output);
            fclose(output);
        }
    }

    free(temp);
    free(filename);
    fclose(input);
}