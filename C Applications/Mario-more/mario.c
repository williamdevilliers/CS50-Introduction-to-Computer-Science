#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n;
    do
    {
        n = get_int("Height: ");
    }
    while (1 > n || 8 < n);
    for (int i = 1; i <= n; i++)
    {
        for (int l = n; l > i; l--)
        {
            printf(" ");
        }
        
        for (int j = 0; j < i; j++)
        {
            printf("#");
        }
        for (int k = 0; k < 2; k++)
        {
            printf(" ");
        }
        for (int h = 0; h < i; h++)
        {
            printf("#");
        }
        printf("\n");
    }
}