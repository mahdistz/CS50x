#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Prompt for start size
    int start_size;
    do
    {
        start_size = get_int("Start size: ");
    }
    while (start_size < 9);

    // Prompt for end size
    int end_size;
    do
    {
        end_size = get_int("End size: ");
    }
    while (end_size < start_size);

    // Calculate number of years until we reach threshold
    if (start_size == end_size)
    {
        printf("Years: 0\n");
    }
    else
    {
        int years = 0;
        for (years = 0; start_size < end_size; years++)
        {
            start_size = start_size + (start_size / 3) - (start_size / 4);
        }

        // Print number of years
        printf("Years: %i\n", years);
    }
}
