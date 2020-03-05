#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "AsInput.h"
#include "AsSymbol.h"
#include "extAndEnt.h"
#include "Code.h"
#include "checkText.h"
#include "convertText.h"
#include "AsData.h"
#include "action.h"
#include "utils.h"
#define SymbolMax 30
#define ErrorJump \
flagError = ON;\
free(command);\
continue;

/*every where there is Discounts: (1), it mean char[81] with 0 in the end of command */
enum Status {OFF,ON};
/*Pointer to lists for all data base*/
dataPointer Head_AsData = NULL;
ptSymbol Head_Symbol = NULL;
codePointer Head_Code = NULL;
ptEAEList Head_EAE = NULL;
short flagError;
char syName[commanSize];

void ride1(FILE *);
void ride2(FILE *);

int main(int argc, char const *argv[])
{	
	int i;
	char *fullFileName = NULL;	
	FILE * file;
	if(argc <= 1)
	{
		printf("No File where typed.\n");
		exit(0);
	}
	for	(i=1; i<argc; i++)
	{			
		fullFileName =NULL;
		fullFileName = concat(argv[i],".as\0");
		if(fullFileName)
		{
			printf(" -- File: %s -- \n",fullFileName);
			file = fopen(fullFileName, "r");
			if (file)
			{
				ride1(file);
				if(flagError == ON)
				{					
					printf(" -- File: %s couldn't be created becuse there are error to fix in it. --\n",fullFileName);
					fclose(file);
					free(fullFileName);
					endSystem();
					continue;
				}
				rewind(file);
				ride2(file);
				if(flagError == ON)
				{					
					printf(" -- File: %s couldn't be created becuse there are error to fix in it. --\n",fullFileName);
					fclose(file);
					free(fullFileName);
					endSystem();
					continue;
				}
				if(printToFile(argv[i]) != 1)
				{
					printf("Error: could not creat output files to: %s.as\n",fullFileName );
				}
				else
				{
					printf(" -- Successfully created all output files for %s.as -- \n",fullFileName);
				}
			   	fclose(file);
			}else{
				printf("Error: The file %s.as dose not exists.\n", argv[i] );
			}
			free(fullFileName);
			endSystem();			
		}
		else
		{
			printf("Dynamic alocation error: couldn't creat file: %s\n", argv[i]);
		}
	}
	return 1;
}

void ride1(FILE *file)
{
	short flagSymbol = OFF;
	int index, end, INTresult, INTresult2, Sy_start, Sy_length, IC = 100, DC = 0, L = 0, lineNumber = 0;
	char *TEXTresult = NULL, *command = NULL;
	flagError = OFF;	
	while((command = getCommand(file)))
	{
		index = 0;
		L = 0;
		flagSymbol = OFF;
		lineNumber++;
		if(!isTextLeft(command,index) || command[jumpSpace(command,0)] == ';')
			continue;		
		if(command[index] == '`')
		{
			printf("Error: in (line: %d) %s\n",lineNumber,(command+index+1) );
			flagError = ON;			
			continue;
		}		
		index = jumpSpace(command,index);
		end = isSymbol(command,index);
		if(end>0)
		{
			flagSymbol = ON;
			Sy_start = index;
			Sy_length = end - index;
			if(Sy_length>=SymbolMax)
			{
				printf("Error: in (line: %d, index: %d) Syntax error, Symbol name can't be longer than: %d.\n",lineNumber,index,SymbolMax);
				ErrorJump	
			}
			index = jumpSpace(command,end+1);			
			if(!isTextLeft(command,index))
			{
				printf("Error: in (line: %d, index: %d) Syntax error, expected a method name or directive after symbol.\n",lineNumber,index);
				ErrorJump
			}
		}
		if(command[index] == '.')
		{
			INTresult = isDirective(command,index);
			if(INTresult<=0)
			{
				printf("Error: in (line: %d, index: %d) Syntax error, unknow directive name.\n",lineNumber,index);
				ErrorJump
			}
			if(INTresult<=3)
			{
				if(flagSymbol)
				{
					flagSymbol = OFF;
					strncpy(syName,(command+Sy_start),Sy_length);			
					syName[Sy_length] = '\0';
					if(checkExist(Head_Symbol,syName))
					{
						printf("Error: in (line: %d, index: %d) Symbol already exist, and have been defined befor.\n",lineNumber,Sy_start);						
						ErrorJump
					}
					if(INTresult == 3)
						INTresult2 = SetNext(&Head_Symbol, command, Sy_start, Sy_length, DC, 1);/*1- for sruct.*/
					else
						INTresult2 = SetNext(&Head_Symbol, command, Sy_start, Sy_length, DC, 0);
					if(INTresult2 == -2)
					{
						printf("Error: in (line: %d, index: %d) Dynamic alocation error, could not add Symbol.\n",lineNumber,Sy_start);
						ErrorJump
					}
				}
				switch(INTresult)
				{
					case 1:
					INTresult2 = addData(command, index, &DC, &Head_AsData);
					if(INTresult2 < 0 && INTresult2 != -2)
					{
						printf("Error: in (line: %d, index: %d) Syntax error, after directive name. (expected: number,number..) note: all number must be between: -512:512 .\n",lineNumber,index);
						ErrorJump
					}					
					break;
					case 2:
					INTresult2 = addString(command, index, &DC, &Head_AsData);
					if(INTresult2 < 0 && INTresult2 != -2)
					{
						printf("Error: in (line: %d, index: %d) Syntax error, after directive name. (expected: \"sum_text\").\n",lineNumber,index);	
						ErrorJump						
					}					
					break;
					case 3:					
					INTresult2 = addStruct(command, index, &DC, &Head_AsData);
					if(INTresult2 < 0 && INTresult2 != -2)
					{
						printf("Error: in (line: %d, index: %d) Syntax error, after directive name. (expected: number,\"sum_text\").\n",lineNumber,index);
						ErrorJump
					}					
					break;
				}
				if(INTresult2 == -2)
				{
					printf("Error: in (line: %d, index: %d) Dynamic alocation error, could not add data.\n",lineNumber,index);					
					ErrorJump
				}
				if(isTextLeft(command,INTresult2))
				{
					printf("Error: in (line: %d, index: %d) Syntax error, unexpected text after directive order.\n",lineNumber,INTresult2);
					ErrorJump
				}				
			}
			else
			{
				if(flagSymbol)
				{
					flagSymbol = OFF;
					printf("Warning in (line: %d, index: %d) unexpected Symbol in this type of directive.\n",lineNumber,Sy_start);				
				}
				if(INTresult == 5)
				{					
					index += externSize;
					if(isTextLeft(command,index))
					{
						index = jumpSpace(command,index);
						INTresult2 = addSymbols(&Head_Symbol, command, index);
						if(INTresult2<0)
						{
							switch(INTresult2)
							{
								case -2:
								printf("Error: in (line: %d, index: %d) Dynamic alocation error, could not add Symbol.\n",lineNumber,Sy_start);
								ErrorJump
								break;
								case -3:								
								printf("Error: in (line: %d, index: %d) Syntax error, unexpected text after adding symbols.\n",lineNumber,index);
								ErrorJump
								break;
								default :
								printf("Error: in (line: %d, index: %d) Syntax error, expected symbol name.\n",lineNumber,index);
								ErrorJump
							}							
						}
					}					
					else
					{
						printf("Error: in (line: %d, index: %d) expected symbol name afted directive: extern.\n",lineNumber,Sy_start);
						ErrorJump
					}					
				}
			}
			free(command);
			continue;
		}
		if(flagSymbol)
		{
			flagSymbol = OFF;
			strncpy(syName,(command+Sy_start),Sy_length);					
			syName[Sy_length] = '\0';
			if(checkExist(Head_Symbol,syName))
			{
				printf("Error: in (line: %d, index: %d) Syntax error, Symbol already exist, and have been defined befor.\n",lineNumber,Sy_start);						
				ErrorJump
			}			
			INTresult2 = SetNext(&Head_Symbol, command, Sy_start, Sy_length, IC, 3);/*3- for code Symbol.*/			
			if(INTresult2 == -2)
			{
				printf("Error: in (line: %d, index: %d) Dynamic alocation error, could not add Symbol.\n",lineNumber,Sy_start);
				ErrorJump
			}
		}
		INTresult = isOrder(command,index);
		if(INTresult<0)
		{
			printf("Error: in (line: %d, index: %d) Syntax error, unknow order name.\n",lineNumber,index);
			ErrorJump
		}
		TEXTresult = countActionList(INTresult, &L, command, index);
		if(TEXTresult != NULL && TEXTresult[0] == '`')
		{
			printf("Error: in (line: %d, index: %d) %s.\n",lineNumber,index,(TEXTresult+1));
			ErrorJump
		}
		IC+=L;
		free(command);
	}
	upgreadeSymbols(Head_Symbol,IC);	
}


void ride2(FILE *file)
{	
	int index, end, INTresult, INTresult2, IC = 100, lineNumber = 0;
	char *TEXTresult = NULL, *command = NULL;
	flagError = OFF;
	while((command = getCommand(file)))
	{
		index = 0;		
		lineNumber++;
		if(!isTextLeft(command,index) || command[jumpSpace(command,0)] == ';')
			continue;		
		if(command[index] == '`')
		{
			printf("Error: in (line: %d) %s\n",lineNumber,(command+index+1) );
			flagError = ON;			
			continue;
		}
		index = jumpSpace(command,index);
		end = isSymbol(command,index);
		if(end>0)
			index = jumpSpace(command,end+1);
		if(command[index] == '.')
		{
			INTresult = isDirective(command,index);			
			if(INTresult == 4)
			{				
				index += entrySize;
				if(isTextLeft(command,index))
				{					
					index = jumpSpace(command,index);
					end = endOfText(command,index);
					if((end-index) > SymbolMax)
					{
						printf("Error: in (line: %d, index: %d) Syntax error, symbol name is too long. Can't pass: %d chars.\n",lineNumber,index,SymbolMax);
						ErrorJump
					}
					TEXTresult = entryToEAE(command,index,end-1);
					if(TEXTresult)
					{
						printf("Error: in (line: %d, index: %d) %s.\n",lineNumber,index,TEXTresult);
						ErrorJump
					}
					if(isTextLeft(command,end))
					{
						printf("Error: in (line: %d, index: %d) Syntax error, unexpected text after symbol name.\n",lineNumber,jumpSpace(command,end));
						ErrorJump
					}
				}
				else
				{
					printf("Error: in (line: %d, index: %d) Syntax error, expected symbol name afted directive: entry.\n",lineNumber,index);
					ErrorJump
				}
			}
			free(command);
			continue;
		}
		INTresult = isOrder(command,index);
		if(INTresult<0)
		{			
			ErrorJump
		}
		TEXTresult = convertOrderToCode(INTresult, command, index, &IC);
		if(TEXTresult != NULL && TEXTresult[0] == '`')
		{
			printf("Error: in (line: %d, index: %d) %s.\n",lineNumber,index,(TEXTresult+1));
			ErrorJump
		}		
		free(command);
	}
	INTresult2 =  dataToCode(IC);
	if(INTresult2 == -2)
	{
		printf("Error: Dynamic alocation error, could not add data list to code list.\n");
		flagError = ON;		
	}
}