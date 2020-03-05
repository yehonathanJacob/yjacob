#include <stdio.h>
#include <ctype.h>
#include "data.h"

int getInt()
{
	int n = 0;
	char c;
	while(isspace(c = getchar()))
		;
	if(c == EOF)
	{
		printf("Error: not enough integer in input.\n");
		return -1;
	}
	else 
	{
		do
		{
			if(c >= '0' && c <= '9')/*is char*/
			{
				n = n*10 + ((int)(c-'0'));				
			}
			else
			{
				printf("Error: the value %c is not an digit.\n", c);
				return -1;
			}
		}while((c = getchar())!= EOF && !isspace(c));
	}	
	return n; 
}
int checkEnd()
{
	char c;
	while(isspace(c = getchar()))
		;
	return (c != EOF)? 0 : 1;
}