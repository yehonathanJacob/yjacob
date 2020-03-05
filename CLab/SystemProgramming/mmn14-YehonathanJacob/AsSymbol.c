#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "AsInput.h"
#include "AsSymbol.h"
#include "checkText.h"

int SetNext(ptSymbol* head, char *command, int from, int length, int adress, short type)
{
	ptSymbol pt;	
	if(*head)
	{		
		pt = *head;		
		while(pt->next)
		{			
			pt = pt->next;
		}		
		pt->next = (ptSymbol)malloc(sizeof(nodeSymbol));		
		pt = pt->next;
	}
	else
	{		
		*head = (ptSymbol)malloc(sizeof(nodeSymbol));
		pt = *head;
	}	
	if(pt && (pt->name = (char *)malloc((length+1)*sizeof(char))))
	{			
		pt->next = NULL;
		pt->name = strncpy(pt->name, command+from,length);
		pt->name[length] = '\0';
		pt->adress = adress;
		pt->type = type;
	}
	else
	{		
		return -2;
	}
	return 1;
}

int checkExist(ptSymbol head, char *name)
{	
	while(head)
	{
		if(strcmp(head->name,name) == 0)
			return 1;
		head = head->next;		
	}
	return 0;
}

ptSymbol GetIfExist(ptSymbol head, char *name)
{
	while(head)
	{
		if(strcmp(head->name,name) == 0)
			return head;
		head = head->next;		
	}
	return NULL;
}

int isSYEmpty(ptSymbol head)
{
	return (head)? 0 : 1;
}

ptSymbol getNextSY(ptSymbol* head)
{
	ptSymbol p;
	if(!isSYEmpty(*head))
	{
		p = *head;
		*head = (*head)->next;
		return p;
	}
	return NULL;
}

void DeleteSymbols(ptSymbol* head)
{
	ptSymbol pt,next;
	if(!isSYEmpty(*head))
	{
		pt = *head;
		while(pt)
		{
			next = pt->next;
			free(pt->name);
			free(pt);
			pt = next;
		}
		*head = NULL;
	}
}

int addSymbols(ptSymbol* head, char *command, int from)
{
	int start,end,count=0;	
	ptSymbol p = NULL;	
	if(*head)
	{
		p = *head;
		while(p->next)		
			p = p->next;	
	}

	while(isTextLeft(command, from) && from>=0)
	{
		start = jumpSpace(command, from);
		end = endOfText(command, start);
		if(end>-1)
		{			
			if(!p)
			{				
				*head = malloc(sizeof(ptSymbol));
				p = *head;
			}
			else
			{				
				p->next=malloc(sizeof(ptSymbol));
				p = p->next;
			}
			if(p && (p->name = malloc(end-start+1)))
			{
				p->next = NULL;
				p->name = strncpy(p->name, command+start, end-start);
				p->name[end-start] = '\0';
				p->adress = 0;
				p->type = 2;
				count++;
				from = jumpBreak(command,end);				
				if((from == -1 && isTextLeft(command, end)) || (from != -1 && !isTextLeft(command, end)))
					return -3;
			}else{
				return -2;				
			}
		}
		else
		{
			return -1;
		}
	}
	return count;
}

void upgreadeSymbols(ptSymbol head, int IC)
{
	while(head)
	{
		if(head->type <= 1)
			head->adress += IC;
		head = head->next;
	}
}