#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "extAndEnt.h"
#include "convertText.h"

int addEAE(ptEAEList * head ,char *Nname , int Naddress,short NisExt)
{	
	ptEAEList pt, temp = (ptEAEList)malloc(sizeof(EAEList));
	if(temp && (temp->address = decimalToMozar(Naddress)))
	{
		temp->isExt = NisExt;
		temp->name = Nname;
		temp->next = NULL;
		if(*head)
		{
			pt = *head;
			while(pt->next)
				pt = pt->next;
			pt->next = temp;
		}
		else
		{
			*head = temp;
		}
	}
	else
	{
		return -2;
	}
	return 1;
}

int isEAEEmpty(ptEAEList head){ return (!head)? 1:0;}

ptEAEList getNextEAE(ptEAEList after){ return after->next;}

char * getEAEList (ptEAEList *head)
{
	int length;
	ptEAEList pt;
	char *newString, *mozar;
	if(*head)
	{
		pt = *head;
		length = strlen(pt->name) + 4;/* 1:sapce, 2-3: mozar, 4: \0*/
		newString = (char *)malloc(length*sizeof(char));
		if(newString)
		{
			strcpy(newString,pt->name);
			strcat(newString, " ");
			mozar = binToMozar(pt->address);
			if(!mozar)
				return "`Dynamic allocatio error.\0";
			strcat(newString, mozar);
			newString[length-1]= '\0';
			return newString;
		}
		else
		{
			return "`Dynamic allocatio error.\0";
		}
		*head = pt->next;
	}
	else{
		return NULL;
	}
}

void DeleteEAE (ptEAEList *head)
{
	ptEAEList pt,temp;
	temp = *head;
	while(temp)
	{
		pt = temp->next;
		free(temp->address);
		free(temp);
		temp = pt;
	}
	*head = NULL;
}

void printListEAE(ptEAEList head){
    ptEAEList temp = head;
    while(temp){
        printf("(%hi,%s,%s)\n", temp->isExt, temp->name, temp->address);
        temp=temp->next;
    }
}