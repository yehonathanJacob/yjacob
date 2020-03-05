typedef struct nodeSymbol * ptSymbol;
typedef struct nodeSymbol{  char *name; int adress;/*in decimal*/ short type;/*0,1,2 or 3*/ ptSymbol next; }nodeSymbol;
int SetNext(ptSymbol* head, char *command, int from, int length, int adress, short type);/*Input: all data needed for new symbol, and head of list. Action: add symbol to list. Discounts: all data is corect. Output: 1 if saccsess, or number<0 otherwise.*/
int checkExist(ptSymbol head, char *name);/*Input: head of list and name to check existient. Output: 1 if exist 0 else.*/
ptSymbol GetIfExist(ptSymbol head, char *name);/*Input: head of list and name to check existient. Output: pointer to node if exist, or NULL else.*/
int isSYEmpty(ptSymbol head);/*Input: head of list. Output: 1 if empty, 0 else.*/
ptSymbol getNextSY(ptSymbol* head);/*Input: head of List. Output: head of list add delete from list.*/
void DeleteSymbols(ptSymbol* head);/*Input: head of List. Output: delete all list*/
int addSymbols(ptSymbol* head, char *command, int from);/*Input: head of list, command and where to start from. Output: adding all Symbol to extern*/
void upgreadeSymbols(ptSymbol head, int IC);/*Input: head of list and IC. Output: updating all symbols adress.*/