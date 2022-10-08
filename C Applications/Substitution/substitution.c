#include <cs50.h>
#include <stdio.h>
#include <math.h>
#include <string.h>

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("missing command-line argument\n");
        return 1;
    }
    else if (strlen(argv[1]) != 26)
    {
        printf("Key must contain 26 characters\n");
        return 1;
    }
    for (int i = 0, n = strlen(argv[1]); i < n; i++)
    {
        if ((argv[1][i] >= 'a' && argv[1][i] <= 'z') || (argv[1][i] >= 'A' && argv[1][i] <= 'Z'))
        {
        }
        else
        {
            printf("Must only contain alphabetic characters\n");
            return 1;
        }
    }
    for (int i = 0, n = strlen(argv[1]); i < n; i++)
    {
        for (int j = i + 1; j < n; j++)
        {
            if (argv[1][i] == argv[1][j])
            {
                printf("Must not contain duplicates\n");
                return 1;
            }
        }
    }
    string plaintext = get_string("plaintext: ");
    printf("ciphertext: ");
    for (int i = 0, n = strlen(plaintext); i < n; i++)
    {
        if (plaintext[i] < 'A' || (plaintext[i] > 'Z' && plaintext[i] < 'a') || plaintext[i] > 'z')
        {
            printf("%c", plaintext[i]);
        }
        if (plaintext[i] >= 'a' && plaintext[i] <= 'z')
        {
            plaintext[i] = plaintext[i] - 96;
            if (argv[1][plaintext[i] - 1] >= 'A' && argv[1][plaintext[i] - 1] <= 'Z')
            {
                argv[1][plaintext[i] - 1] += 32;
            }
            printf("%c", argv[1][(int) plaintext[i] - 1]);
        }
        if (plaintext[i] >= 'A' && plaintext[i] <= 'Z')
        {
            plaintext[i] = plaintext[i] - 64;
            if (argv[1][plaintext[i] - 1] >= 'a' && argv[1][plaintext[i] - 1] <= 'z')
            {
                argv[1][plaintext[i] - 1] -= 32;
            }
            printf("%c", argv[1][(int) plaintext[i] - 1]);
        }
    }
    printf("\n");
    return 0;
}