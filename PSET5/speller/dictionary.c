// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Choose number of buckets in hash table
const unsigned int N = 100000;

// Hash table
node *table[N];
int dictionary_size = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // Hash word to obtain hash value
    int hash_value = hash(word);
    // Access linked list at that index in hash table
    node *m = table[hash_value];
    // Traverse linked list, looking for word (strcasecomp)
    while (m != NULL)
    {
        if (strcasecmp(word, m->word) == 0)
        {
            return true;
        }
        m = m->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // Function should take a string and return an index
    // This hash function adds the ASCII values of all characters in the word together
    long sum = 0;
    for (int j = 0; j < strlen(word); j++)
    {
        sum += tolower(word[j]);
    }
    return sum % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open dictionary file
    FILE *dictionary_pointer = fopen(dictionary, "r");
    // Check if null
    if (dictionary == NULL)
    {
        printf("Unable to open %s\n", dictionary);
        return false;
    }
    // Initialise word array
    char next_word[LENGTH + 1];
    // Read strings from file one at a time
    while (fscanf(dictionary_pointer, "%s", next_word) != EOF)
    {
        // Create new node for each word
        node *m = malloc(sizeof(node));
        if (m == NULL)
        {
            return false;
        }
        // copy word into node using strcopy
        strcpy(m->word, next_word);
        // Hash word to obtain hash value
        int hash_value = hash(next_word);
        // Insert node into hash table at that location
        m->next = table[hash_value];
        table[hash_value] = m;
        dictionary_size++;
    }
    // Close file
    fclose(dictionary_pointer);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return dictionary_size;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // Iterate over hash table and free nodes in each linked list
    for (int h = 0; h < N; h++)
    {
        // Assign cursor
        node *m = table[h];
        // Loop through linked list
        while (m != NULL)
        {
            // Make temp equal cursor;
            node *temp = m;
            // Point cursor to next element
            m = m->next;
            // free temp
            free(temp);
        }
        if (m == NULL && h == N - 1)
        {
            return true;
        }
    }
    return false;
}
