#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

float calculateColemanLiau(char *text);

int main(void)
{
    char *text;
    text = get_string("Text: ");
    float index = calculateColemanLiau(text);
    int colemanLiauIndex = round(index);
    if (colemanLiauIndex < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (colemanLiauIndex >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", colemanLiauIndex);
    }
}

float calculateColemanLiau(char *text)
{
    int letters = 0, words = 0, sentences = 0;

    // Iterate through each character in the text
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (isalpha(text[i]))
        {
            // Count the number of letters in the text
            letters++;
        }
        else if (isspace(text[i]))
        {
            // Count the number of words in the text
            words++;
        }
        else if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            // Count the number of sentences in the text
            sentences++;
        }
    }

    // Increment words for the last word in the text
    words++;

    // Calculate the Coleman-Liau index
    float L = (float) letters / words * 100;
    float S = (float) sentences / words * 100;
    float index = 0.0588 * L - 0.296 * S - 15.8;

    return index;
}