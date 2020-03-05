typedef struct EAEList * ptEAEList; /*Pointer to node*/
typedef struct EAEList
{
	short isExt;/*0 or 1*/
	char *name;/*name of symbol*/
	char *address;/*address of symbol in Mozar*/
	ptEAEList next; /*Pointer to next*/
}EAEList;

int addEAE(ptEAEList * head ,char *name , int adress,short isExt); /*Input: pointer to head of EAEList, and all data needed for new node. Output: 1 if succses to enter it, or number<0 otherwise*/
int isEAEEmpty(ptEAEList head);/*Input: pointer to head of EAEList, Output: 1 if empty, or number<0 otherwise*/
ptEAEList getNextEAE(ptEAEList after); /*Input: pointer to EAEList, Output: pointer to next node*/
char * getEAEList (ptEAEList *head);/*Input: pointer to head of EAEList, Output: head of list as a string to print to file, and delete head of file.*/
void DeleteEAE (ptEAEList *head);/*Input: pointer to head of EAEList. Delete all list, no output*/
void printListEAE(ptEAEList head);/*Input: pointer to head of EAEList. Ouyput: print list to screen*/