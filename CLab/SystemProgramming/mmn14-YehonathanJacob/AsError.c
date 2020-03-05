#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "AsError.h"

void setLast(ptError *p, char *text, int line)
{
	ptError pt;
	int length;
	if(*p)
	{		
		pt = *p;		
		while(pt->next)
		{			
			pt = pt->next;
		}		
		pt->next = (ptError)malloc(sizeof(nodeError));
		pt = pt->next;
	}
	else
	{		
		*p = (ptError)malloc(sizeof(nodeError));
		pt = *p;
	}	
	length = strlen(text);
	printf("length: %d\n",length );
	if(pt && (pt->data = (char *)malloc(length)))
	{	
		pt->lineNum = line;
		pt->next = NULL;
		strcpy(pt->data, text+1);
		pt->data[length-1] = '\0';
	}
	else
	{		
		printf("Run time error: can't alocate memory for text.\n");
	}	
}

int isEREmpty(ptError pt)
{
	return (pt)? 0 : 1;
}

void printHead(ptError *p)
{
	if(!isEREmpty(*p))
	{
		printf("\nError: (line: %d) %s\n",(*p)->lineNum,(*p)->data);
		*p = (*p)->next;
	}	
}

void DeleteErrors(ptError *p)
{
	ptError pt,next;
	if(!isEREmpty(*p))
	{
		pt = *p;
		while(pt)
		{
			next = pt->next;
			free(pt->data);
			free(pt);
			pt = next;
		}
		*p = NULL;
	}	
}