#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
}
pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if(argc<2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if(candidate_count>MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for(int i = 0;i<candidate_count;i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for(int i = 0;i<candidate_count;i++)
    {
        for(int j = 0;j<candidate_count;j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for(int i = 0;i<voter_count;i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for(int j = 0;j<candidate_count;j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if(!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    for(int i = 0;i<pair_count;i++)
    {
        printf("Before sort:\npairs[%i].winner = %i\npairs[%i].loser = %i\n", i, pairs[i].winner, i, pairs[i].loser);
    }
    sort_pairs();
    for(int i = 0;i<pair_count;i++)
    {
        printf("After sort:\npairs[%i].winner = %i\n pairs[%i].loser = %i\n", i, pairs[i].winner, i, pairs[i].loser);
    }
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    for(int i = 0;i<candidate_count;i++)
    {
        if(!strcmp(name, candidates[i]))
        {
            ranks[rank] = i;
            return true;
        }
    }
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    for(int i = 0;i<candidate_count;i++)
    {
        for(int j = (1 + i);j<candidate_count;j++)
        {
            preferences[ranks[i]][ranks[j]]++;
        }
    }
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    for(int i = 0;i<candidate_count;i++)
    {
        for(int j = 0;j<candidate_count;j++)
        {
            if(!(i==j) && (preferences[i][j]>preferences[j][i]))
            {
                pairs[pair_count].winner = i;
                pairs[pair_count].loser = j;
                pair_count++;
            }
        }
    }
    return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    int counter = -1;
    do
    {
        for(int i = 0;i<(pair_count - 2);i++)
        {
            int winner1 = pairs[i].winner;
            int loser1 = pairs[i].loser;
            int winner2 = pairs[i + 1].winner;
            int loser2 = pairs[i + 1].loser;
            counter = 0;
            if(preferences[winner1][loser1]<preferences[winner2][loser2])
            {
                int twinner = pairs[i].winner; //twinner and tloser are the temporary placeholders
                int tloser = pairs[i].loser;
                pairs[i].winner = pairs[i + 1].winner;
                pairs[i].loser = pairs[i + 1].loser;
                pairs[i + 1].winner = twinner;
                pairs[i + 1].loser = tloser;
                counter++;
            }
        }
    }
    while (counter != 0);
    return;
}

bool cycle(int end, int cycle_start)
{
    if(end == cycle_start)
    {
        return true;
    }
    for(int i = 0;i<candidate_count;i++)
    {
        if(locked[end][i])
        {
            if(cycle(i, cycle_start))
            {
                return true;
            }
        }
    }
    return false;
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    for(int i = 0;i<pair_count;i++)
    {
        if(!cycle(pairs[i].loser, pairs[i].winner))
        {
            locked[pairs[i].winner][pairs[i].loser] = true;
        }
    }
    return;
}

// Print the winner of the election
void print_winner(void)
{
    for(int i = 0;i<candidate_count;i++)
    {
        int false_count = 0;
        for(int j = 0;j<candidate_count;j++)
        {
            if(locked[j][i] == false)
            {
                false_count++;
                if(false_count == candidate_count)
                {
                    printf("%s\n", candidates[i]);
                }
            }
        }
    }
    return;
}