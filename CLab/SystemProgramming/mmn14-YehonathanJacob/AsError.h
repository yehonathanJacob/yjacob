typedef struct nodeError * ptError;
typedef struct nodeError
{
	int lineNum;
	char *data;
	ptError next;
}nodeError;
void setLast(ptError *, char *, int);/*Input: data for new node, and pointer to head.*/ 
int isEREmpty(ptError);/*Input: head of list. Output: 1 if empty, 0 else.*/
void printHead(ptError *);/*Input: head of List. Output: pirnt out head of list*/
void DeleteErrors(ptError *);/*Input: head of List. Output: delete all list*/