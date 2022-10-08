#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

int main(void)
{
    double letters = 0;
    double words = 1;
    double sentences = 0;
    string text = get_string("Text: ");
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if ((text[i] >= 'a' && text[i] <= 'z') || (text[i] >= 'A' && text[i] <= 'Z'))
        {
            letters++;
        }
    }
    for (int j = 0, n = strlen(text); j < n; j++)
    {
        if (text[j] == ' ')
        {
            words++;
        }
    }
    for (int k = 0, n = strlen(text); k < n; k++)
    {
        if (text[k] == '.' || text[k] == '!' || text[k] == '?')
        {
            sentences++;
        }
    }
    double L = letters * 100 / words;
    double S = sentences * 100 / words;
    double index = 0.0588 * L - 0.296 * S - 15.8;
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %0.0f\n", index);
    }
}