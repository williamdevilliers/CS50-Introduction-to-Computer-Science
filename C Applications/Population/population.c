#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n;
    int m;
    int y = 0;
    do
    {
        n = get_int("Start size: ");
    }
    while (9 > n);
    do
    {
        m = get_int("End size: ");
    }
    while (n > m);
    while (n < m)
    {
           n = n + (n / 3) - (n / 4);
           y++;
    }
    printf("Years: %i", y);
}