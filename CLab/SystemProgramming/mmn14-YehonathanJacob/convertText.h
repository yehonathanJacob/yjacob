#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#ifndef mask
#define mask 1
#endif

int binToDecimal(char *bin);                        /* Receives an array of chars holding a number in its binary form, and returns the number in decimal*/
char * decimalToBin(int num);                       /* Receives a number and returns an array holding the number in binary form */
char *binToMozar(char *bin);                        /* Receives a char array holding a number in binary, and returns an array holding the number in the special 32 base */
char * decimalToMozar(int num);                     /* Receives a number, and returns an array holding the number in the special 32 base */
char* concat(const char *s1, const char *s2);       /* input: two strings.  Output: one string that is the combination of both strings*/
int textToNum(char *text, int from, int end);       /* Input: Receives a string and integer 'from', and integer 'end'.  Output: A number that is a substring of this string from 'from' to 'end'*/

