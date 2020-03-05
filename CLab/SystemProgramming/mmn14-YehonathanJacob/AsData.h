#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <ctype.h>
#include "checkText.h"
#include "convertText.h"
#include "AsInput.h"
#ifndef directiveSize
#define directiveSize
#define stringSize 7
#define structSize 7
#define dataSize 5
#define externSize 7
#define entrySize 7
#endif


typedef struct dataList * dataPointer;
typedef struct dataList{
    int data; /* in decimal */
    int DC; /*in decimal*/
    dataPointer next;

} dataList;

/*(1) returns 1 if all worked well, -2 if there was a dynamic allocation error and -1 otherwise*/



int addNode(dataPointer *head , int number, int * DC);  /*Input: a pointer to a pointer to a dataList structure, a number which is the data and a pointer to DC
                                                         *Output: (1) above
                                                         *Action: First, it creates a new dataList structure which contains the inputted number and DC, then if there is a linked list which the inputted dataList structure as its head, it adds it to the end of the list, otherwise the function sets it to be the head of the list. The function also adds 1 to the given DC*/

int addString(char *command, int from, int *DC, dataPointer *head);     /*Input: a string which contains a string (with quotations), an integer that represents the starting point, a pointer to DC, and a pointer to the head of the list
                                                                         *Output: If the string was successfully added to the dataList, the function returns the position after the second quotations, else -2 if there was a dynamic allocation error and -1 otherwise
                                                                         * Action: The functions adds every letter to the dataList structure, including the '\0' character*/

int addStruct(char *command, int from, int *DC, dataPointer *head);     /*Input: a string which represents a struct directive, an integer from, a pointer to DC and a pointer to the head of the dataList
                                                                         *Output: if successful in adding the struct, it returns the index after all parameters. else, it returns -2 if there was a dynamic allocation error and -1 otherwise
                                                                         *Action: First it adds the number to the dataList, and then it adds each letter of the string to the dataList, including '\0'*/

int addData(char *command, int from, int *DC, dataPointer*head);        /*Input: Input: a string which represents a data directive, an integer from, a pointer to DC and a pointer to the head of the dataList
                                                                         *Output: if all the numbers have been added successfully, than the function returns the index after all the numbers, else return -2 if there was a dynamic allocation error and -1 otherwise.
                                                                         * Action: adds all the numbers provided in the .data directive to the dataList*/

void deleteDataList(dataPointer * head);                                  /*Input: a pointer to the head of the dataList
                                                                         *Output: none
                                                                         * Action: frees the dataList*/

void printDataList(dataPointer head); /*prints the list*/