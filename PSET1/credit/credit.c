#include <cs50.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void)
{
    long credit_cart_no;
    do
    {
        credit_cart_no = get_long("Number: ");
    }
    while (credit_cart_no <= 0);

    char credit_cart[16];

    // Convert the long number to string
    sprintf(credit_cart, "%ld", credit_cart_no);
    // Calculate length of the string
    int cart_length = strlen(credit_cart);

    long credit_card = credit_cart_no;
    int mod1;
    int mod2;
    int sum1 = 0;
    int sum2 = 0;
    int total = 0;

    while (credit_card >= 1)
    {
        mod1 = credit_card % 10;
        credit_card /= 10;

        sum1 += mod1;

        mod2 = credit_card % 10;
        mod2 = mod2 * 2;
        if (mod2 > 9)
        {
            mod2 = (mod2 / 10) + (mod2 % 10);
        }
        credit_card /= 10;

        sum2 += mod2;
    }
    total = sum1 + sum2;
    printf("total: %i\n", total);

    if (total % 10 == 0)
    {
        long number = credit_cart_no;
        if (cart_length != 13 && cart_length != 15 && cart_length != 16)
        {
            printf("INVALID\n");
        }
        else if (cart_length == 15)
        {
            int two_first_num = number / pow(10, 13);
            if (two_first_num == 34 || two_first_num == 37)
            {
                printf("AMEX\n");
            }
        }
        else if (cart_length == 16)
        {
            int two_first_num = number / pow(10, 14);
            int first_num = number / pow(10, 15);

            if (two_first_num == 51 || two_first_num == 52 || two_first_num == 53 || two_first_num == 54 || two_first_num == 55)
            {
                printf("MASTERCARD\n");
            }
            else if (first_num == 4)
            {
                printf("VISA\n");
            }
        }
        else if (cart_length == 13)
        {
            int first_num = number / pow(10, 12);
            if (first_num == 4)
            {
                printf("VISA\n");
            }
        }
    }
    else
    {
        printf("INVALID\n");
    }
}
