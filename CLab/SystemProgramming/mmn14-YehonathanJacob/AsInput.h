#ifndef commanSize
#define commanSize 81
#endif
char *getCommand(FILE *);/*Input: pointer to file. Output: char[81] that in the end of comman: /0. Discounts: file is open for reading*/
char getNext(FILE *);/*Input: pointer to file. Output: next char. Discounts: file is open for reading*/
void setNext(char c);/*Input: pointer to file, and next char.*/
int jumpSpace(char *command, int from);/*Input: pointer to arry, and starting poin. Output: point after starting text. Discounts: (1)*/
int jumpBreak(char *command, int from);/*Input: pointer to arry, and starting poin. Output: point after comma. Discounts: (1)*/
int isTextLeft(char *command, int from);/*Input: pointer to arry, and starting poin. Output: if there is text left? 1 : 0. Discounts: (1)*/
int endOfText(char *command, int from);/*Input: pointer to arry, and starting poin. Output: point of end of text (comma, apostrophes or space). Discounts: (1)*/