#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "AsInput.h"
char buffer[100];
static int index = -1;

char *getCommand(FILE *fp1)/*Input: pointer to file. Output: char[81] that in the end of comman: /0. Discounts: file is open for reading*/
{
	char c;
	char *arr;
	int i;
	if((c=getNext(fp1))!= EOF)
		setNext(c);
	else
		return NULL;
	arr = (char *)malloc(commanSize*sizeof(char));
	if(arr)
	{
		i = 0;
		while((c = getNext(fp1)) != EOF && c != '\n' && i<(commanSize-1))
		{
			arr[i] = c;
			i++;
		}
		arr[i] = '\0';
		if(i <= (commanSize-1) && c!= EOF && c != '\n')
		{
			setNext(c);
			while((c = getNext(fp1)) != EOF && c != '\n')
				;
			if(c == EOF)			
				setNext(c);			
			return "`Syntax error, too much long command.\0";
		}
		else
			return arr;

	}
	else
	{
		return "`Dynamic allocatio error, can not create space.\0";
	}	
}

char getNext(FILE *fp1)/*Input: pointer to file. Output: next char. Discounts: file is open for reading*/
{
	if(index>-1)
	{
		return buffer[index--];
	}
	return getc(fp1);
}

void setNext(char c)/*Input: next char.*/
{
	buffer[++index] = c;
}

int jumpSpace(char *command, int from)/*Input: pointer to arry, and starting poin. Output: point after starting text. Discounts: (1)*/
{
	char c;
	while((c = command[(from)]) != '\0' && isspace(c))
		from++;
	return from;
}

int jumpBreak(char *command, int from)/*Input: pointer to arry, and starting poin. Output: point after comma, or -1 if not found Discounts: (1)*/
{
	from = jumpSpace(command,from);
	if(command[from] == ',')
	{
		from++;
		return from;
	}
	else
	{
		return -1;
	}
}

int isTextLeft(char *command, int from)/*Input: pointer to arry, and starting poin. Output: if there is text left? 1 : 0. Discounts: (1)*/
{
	from = jumpSpace(command,from);
	return (command[from] != '\0')? 1 : 0;	
}

int endOfText(char *command, int from)/*Input: pointer to arry, and starting poin. Output: point of end of text (comma, apostrophes or space). Discounts: (1)*/
{
	char c;
	while((c = command[(from)]) != '\0' && !isspace(c) && (c != ','))
		from++;
	return from;
}