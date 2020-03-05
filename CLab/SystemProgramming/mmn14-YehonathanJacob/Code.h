#include <stdio.h>
#include <stdlib.h>
#include "convertText.h"

typedef struct codeList * codePointer;
typedef struct codeList{
    int address;             /* in decimal*/
    char *bin;          /*the character array represents a binary number*/
    codePointer next;
} codeNode;


int isEmptyCode(codePointer head);                              /*Input: a pointer to the head of the codeList
                                                                 *Output: 1 if the codeList is empty, -1 otherwise
                                                                 * Action: checks if the list has nodes*/

int addCode(codePointer * head ,int address ,char *bin);        /*Input: a pointer to a pointer to the head of the codeList, the address of the new code and the code, represented in binary and in length 10
                                                                *Output: 1 if a new node with the given data was added successfully, -2 if there was a problem with dynamic allocation, and -1 otherwise
                                                                * Action: adds a new node with the given data to the end of the codeList*/

codePointer getNextCode(codePointer current);                       /*Input: a pointer to a node in the list
                                                                 *Output: a pointer to the node after the given pointer
                                                                 * Action: returns a pointer to the node that is the next after the given node*/

char * getCode(codePointer * head);                             /*Input: a pointer to the pointer to the head of the list
                                                                 *Output: an array of chars, or an error if there was a problem with dynamic allocation
                                                                 * Action: the function removes the head, and put in the char array the following: First, it puts in the first two slots the address that was in the head node in the weird base 32, then a white space, and then in the next 3 slots it puts the number in the code array (which is in binary) in the weird base 32 followed buy a null ('\0') character*/

void deleteListCode(codePointer * head);                            /*Input: a pointer to the head of the codeList
                                                                 *Output: none
                                                                 * Action: frees the codeList*/