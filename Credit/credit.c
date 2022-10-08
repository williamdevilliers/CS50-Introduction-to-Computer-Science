#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    long cardnum;
    long cardnum1;
    int checksum;
    double ndigits;
    int firstnumber;
    int firsttwonumbers;
    int thedouble;
    do
    {
        cardnum = get_long("Number: ");
        checksum = 0;
        ndigits = 0;
        
    }
    while (cardnum < 1);
    cardnum1 = cardnum;
    do
    {
        ndigits++;
        cardnum1 /= 10;
    }
    while (cardnum1 > 0);
    firstnumber = cardnum / (1 * pow(10, ndigits - 1));
    firsttwonumbers = cardnum / (1 * pow(10, ndigits - 2));
    for (int i = 0; i <= cardnum; i++)
    {
        thedouble = (cardnum % 100) / 10 * 2;
        checksum += (thedouble % 100) / 10 + thedouble % 10;
        checksum += (cardnum % 10);
        cardnum /= 100;
    }
    checksum += cardnum;
    if (ndigits == 15 && (firsttwonumbers == 34 || firsttwonumbers == 37) && checksum % 10 == 0)
    {
        printf("AMEX\n");
    }
    else if (ndigits == 16 && (51 <= firsttwonumbers && firsttwonumbers <= 55) && checksum % 10 == 0)
    {
        printf("MASTERCARD\n");
    }
    else if ((ndigits == 16 || ndigits == 13) && firstnumber == 4 && checksum % 10 == 0)
    {
        printf("VISA\n");
    }
    else
    {
        printf("INVALID\n");
    }
}