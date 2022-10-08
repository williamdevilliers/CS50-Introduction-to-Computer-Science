// Implements a dictionary's functionality

#include "dictionary.h"
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <strings.h>
#include <stdint.h>
#include <ctype.h>

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

unsigned int hashValue;
unsigned int word_count;

// Number of buckets in hash table
const unsigned int N = 1337;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    hashValue = hash(word);
    node *k = table[hashValue];
    while (k != NULL)
    {
        if (strcasecmp(word, k->word) == 0)
        {
            return true;
        }
        k = k->next;
    }
return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    long total = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        total += tolower(word[i]);
    }
    return total % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    FILE *dpoint = fopen(dictionary, "r");
    if (dpoint == NULL)
    {
        return false;
    }
    char nextword[LENGTH+1];
    while (fscanf(dpoint, "%s", nextword) != EOF)
    {
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }
        strcpy(n->word, nextword);
        hashValue = hash(nextword);
        n->next = table[hashValue];
        table[hashValue] = n;
        word_count++;
    }
    fclose(dpoint);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    if (word_count > 0)
    {
        return word_count;
    }
    return 0;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *k = table[i];
        while (k)
        {
            node *tmp = k;
            k = k->next;
            free(tmp);
        }
        if (i == N - 1 && k == NULL)
        {
            return true;
        }
    }
    return false;
}
