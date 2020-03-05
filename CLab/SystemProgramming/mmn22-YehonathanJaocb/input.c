#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
char buffer[100];
void jumpSpace();
static int index = -1;

static char getNext()
{
	if(index>-1)
	{
		return buffer[index--];
	}
	return getchar();
}

static void setNext(char c)
{
	buffer[++index] = c;
}

double *getNumer()/*expect:-int.int*/
{	
	double *num = NULL;
	char c;
	int signal = 1;
	int i = 0;
	char *buf = (char *)calloc(100,sizeof(char));
	if(buf)
	{
		num = (double *)malloc(sizeof(double));
		if(num)
		{
			jumpSpace();
			c = getNext();			
			if(c == EOF || c == '\n')
			{
				printf("Error(20): Unexpected end of comand\n");
				setNext(c);				
				free(buf);
				free(num);
				return NULL;				
			}	
			if(c == '-')
			{
				buf[i] = c;
				i++;
				c = getNext();
			}
			do
			{				
				if(c >= '0' && c <= '9')/*is char*/
				{
					buf[i] = c;
					i++;
				}
				else if(signal && c == '.')
				{
					buf[i] = c;
					i++;
					signal = 0;			
				}else{
					setNext(c);
					printf("Error(20): Unexpected char in number:%c\n",c);
					free(buf);
					free(num);
					return NULL;
				}
			}while((c=getNext()) != EOF && !isspace(c) && i<=100 && c != ',');
			setNext(c);
			*num = atof(buf);	
			free(buf);
		}else{ printf("Error(21): Unable to read next number\n");}
	}else{ printf("Error(22): Unable to read next number\n");}
	return num;
}

char *getStr()
{
	char *buffer = NULL;
	char c;
	int i = -1;
	jumpSpace();
	buffer = (char *)calloc(100,sizeof(char));
	if(buffer)
	{
		while((c = getNext()) != EOF && !isspace(c) && i < 100  && c != ',')
		{
			i++;
			*(buffer+(i)) = c;
		}
		setNext(c);
		if(i<0)/*case no string*/
		{
			free(buffer);
			return NULL;
		}
	}else
	{
		return NULL;
	}
	return buffer;
}
int checkend()
{
	char c= getNext();
	setNext(c);
	if(c == EOF)
		return 1;
	else 
		return 0;
}
int jumpStep() /*look for ',' and jump over it, return 1 if founded*/
{
	char c;
	jumpSpace();
	c = getNext();
	if(c == ',')
	{
		return 1;
	}
	else
	{
		setNext(c);
		return 0;
	}
}
int runToEnd()/*if until end of comand ther is a char that is not space*/
{
	char c;
	int back = 1;
	while((c=getNext()) != EOF && c != '\n')
	{
		if(!isspace(c))
			back = 0;
	}
	if(c == EOF)
	{
		setNext(EOF);
	}
	return back;
}
void jumpSpace()
{
	char c;
	while((c = getNext()) != EOF && isspace(c) && c != '\n')
		;	
	setNext(c);	
}