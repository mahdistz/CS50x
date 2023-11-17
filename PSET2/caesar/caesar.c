#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    int len = strlen(argv[1]);
    for (int i = 0; i < len; i++)
    {
        if (isalpha(argv[1][i]))
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }
    string text;
    text = get_string("plaintext:  ");
    int key = atoi(argv[1]); // convert string to integer

    printf("ciphertext: ");

    char cipher;
    int textLen = strlen(text);
    for (int k = 0; k < textLen; k++)
    {
        int c = text[k];
        if (isalpha(c))
        {
            cipher = c + key % 26;
            if (!(islower(cipher) || isupper(cipher)))
            {
                cipher -= 26;
            }
        }
        else
        {
            cipher = c;
        }
        printf("%c", cipher);
    }
    printf("\n");
    return 0;
}