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
#include <unistd.h>
#define SymbolMax 30

/*Pointer to lists for all data base*/
extern dataPointer Head_AsData;
extern ptSymbol Head_Symbol;
extern codePointer Head_Code;
extern ptEAEList Head_EAE;

char *addCodeToDB(unsigned int arr[],int n,int *IC)
{
	int i;
	char *bin;
	for(i=0;i<n;i++)
	{
		bin = decimalToBin(arr[i]);
		if(bin[0] == '%' || addCode(&Head_Code,*IC,bin) == -2)
			return "`Dynamic allocatio error.\0";
		(*IC)+=1;
	}
	return NULL;

}

int printToFile(const char *fileName)
{
	int flagEnt=0,flagExt=0;
	char *fnameOB = NULL,*fnameENT = NULL,*fnameEXT = NULL,*textToPrint = NULL;
	FILE *fp1,*fp2;
	codePointer ptCode;
	ptEAEList ptEAE;	
	if(isEmptyCode(Head_Code))
	{		
		fnameOB = concat(fileName,".ob\0");		
		if(!fnameOB || !(fp1 = fopen(fnameOB,"w")))
			return -1;
		fprintf(fp1,"m\tf\n");
		ptCode = Head_Code;
		while(ptCode)
		{
			textToPrint = getCode(&ptCode);			
			if(!textToPrint)
			{
				fclose(fp1);
				unlink(fnameOB);
				return -1;
			}
			fprintf(fp1,"%s\n",textToPrint);
		}
		fclose(fp1);
	}
	if(!isEAEEmpty(Head_EAE))
	{
		ptEAE = Head_EAE;
		while(ptEAE)
		{
			flagEnt = (flagEnt || !(ptEAE->isExt));
			flagExt = (flagExt || (ptEAE->isExt));
			ptEAE = ptEAE->next;
		}
		if (flagExt)
		{
			fnameEXT = concat(fileName,".ext\0");
			if(!fnameEXT || !(fp1 = fopen(fnameEXT,"w")))
			{
				unlink(fnameOB);
				return -1;
			}
		}
		if(flagEnt)
		{
			fnameENT = concat(fileName,".ent\0");
			if(!fnameENT || !(fp2 = fopen(fnameENT,"w")))
			{
				unlink(fnameOB);
				if(fnameEXT) {unlink(fnameEXT);}
				return -1;
			}
		}

		ptEAE = Head_EAE;
		while(ptEAE)
		{
			if(ptEAE->isExt)
			{
				fprintf(fp1,"%s\t%s\n",ptEAE->name,ptEAE->address);
			}else
			{
				fprintf(fp2,"%s\t%s\n",ptEAE->name,ptEAE->address);
			}
			ptEAE = ptEAE->next;
		}
		if (flagExt)
			fclose(fp1);
		if(flagEnt)
			fclose(fp2);
	}

	return 1;
}

int dataToCode(int IC)
{
	codePointer last = Head_Code,temp;
	dataPointer head = Head_AsData;
	char *bin;
	if(last)
		while(last->next)
			last = last->next;
	else
	{
		if(head)
		{
			if((temp = (codePointer)malloc(sizeof(codeNode))) && (bin = decimalToBin(head->data)))
			{
				temp->address = IC+head->DC;
				temp->bin = bin;
				Head_Code = temp;
				last = temp;
			}
			else{
				return -2;
			}
		}
	}

	while(head)
	{
		if((temp = (codePointer)malloc(sizeof(codeNode))) && (bin = decimalToBin(head->data)))
		{
			temp->address = IC+head->DC;
			temp->bin = bin;
			last->next = temp;
			last = last->next;
		}
		else{
			return -2;
		}
		head = head->next;
	}
	return last->address;
}

char *convertOrderToCode(int NumAction, char *command, int from, int *IC)
{
	unsigned int nextLine[5] = {0,0,0,0,0};/*there max:5 lines that we will need to add.*/
	int numberOfLine = 0;/*to know how many lines to convert to actual code.*/
	int result;
	int Addressing1,Addressing2,end,i;
	static char SyName[SymbolMax];
	ptSymbol temp;
	/*frist line*/
	numberOfLine++;
	nextLine[0]|= (NumAction<<6);
	from+=3;
	if(NumAction>=14)
	{
		if(NumAction == 15)
			from+=2;			
		if(isTextLeft(command,from))
			return "`Syntax error, unexpected text afer action name.\0";
		else
			return addCodeToDB(nextLine,numberOfLine,IC);
	}
	/*second line*/
	if(!isTextLeft(command,from))
		return "`Syntax error, expected operate after action name.\0";
	from = jumpSpace(command,from);
	Addressing1 = getAddressing(command,from);	
	switch (Addressing1)
	{
		case 0:/*meens command[from] = "#..."*/
		if(NumAction<=3 || NumAction == 12){
			from++;
			end = 0;
			end = isNumber(command,from);
			if(end>0)/*there is a valid number between from to end*/
			{
				result = textToNum(command,from,end-1);
				if(result>128 || result<-128)/*we have only 8 bit + 2 for type of coadind*/
					return "`Syntax error, number can be between 128 to -128 in this action.\0";	
				nextLine[numberOfLine]|= ((result<<2)&(-4));
				/*int nextLine[0] in adresing we live it '0'.*/
				numberOfLine++;
				from = end;
			}
			else
				return "`Syntax error, expected a number after '#' in first operate.\0";
		}
		else
			return "`Syntax error, Addressing number: 0, can't be in first operate, at this action.\0";
		break;
		case 1:
		end = 0;
		end = endOfText(command, from);
		if(end - from >= SymbolMax)
			return "`Syntax error, too much long text afte action name. Symbol name can't be more then 30 chars.\0";
		for(i=0;i<end - from;i++)
			SyName[i] = command[from+i];
		SyName[i] = '\0';
		if((temp = GetIfExist(Head_Symbol,SyName)))
		{
			nextLine[numberOfLine]|= (temp->adress)<<2;
			if(temp->type != 2)/*meens ENTERNAL sdymbol*/
				nextLine[numberOfLine]|= 2;/*10*/
			else				/*meens EXTERNAL sdymbol*/
			{
				nextLine[numberOfLine]|= 1;/*01*/
				if( addEAE(&Head_EAE, temp->name , (*IC) + numberOfLine, 1) == -2)
					return "`Dynamic allocatio error.\0";
			}
			if(NumAction<=3 || NumAction == 6)/*check if it is target or source*/
				nextLine[0]|= 1<<4;
			else
				nextLine[0]|= 1<<2;
			/*int nextLine[0] in adresing we live it '0'.*/
			numberOfLine++;
			from = end;
		}
		else
			return "`Syntax error, Symbol tyiped in fisrt action dosn't exist.\0";
		break;
		case 2:/*meens THER IS a '.' */
		end = 0;
		while(command[from+end] != '.')
			end++;
		if(end >= SymbolMax)
			return "`Syntax error, too much long text afte action name. Symbol name can't be more then 30 chars.\0";
		for(i=0;i<end;i++)
			SyName[i] = command[from+i];
		SyName[i] = '\0';		
		if((temp = GetIfExist(Head_Symbol,SyName)))
		{
			if(temp->type == 1 || temp->type == 2)
			{
				from += end+1;
				nextLine[numberOfLine]|= (temp->adress)<<2;
				numberOfLine++;
				if(command[from] == '1' || command[from] == '2')
					nextLine[numberOfLine]|= (command[from] - '0')<<2;
				else
					return "`Syntax error, expected 1 or 2 after: '.' in struct name in first operate.\0";
				if(temp->type != 2){/*meens ENTERNAL sdymbol*/				
					nextLine[numberOfLine-1]|= 2;/*10*/
					nextLine[numberOfLine]|= 0;/*00*/
				}
				else{				/*meens EXTERNAL sdymbol*/
					nextLine[numberOfLine-1]|= 1;/*01*/
					nextLine[numberOfLine]|= 0;/*00*/
					if( addEAE(&Head_EAE, temp->name , (*IC) + numberOfLine, 1) == -2)
						return "`Dynamic allocatio error.\0";
				}

				if(NumAction<=3 || NumAction == 6)/*check if it is target or source*/
					nextLine[0]|= 2<<4;
				else
					nextLine[0]|= 2<<2;				
				numberOfLine++;
				from++;
			}
			else
				return "`Syntax error, expected symbol of struct.\0";
		}
		else
			return "`Syntax error, Symbol (struct) tyiped in fisrt action dosn't exist.\0";
		break;
		case 3:/*meens command[from] = "r*..." */
		if(NumAction != 6)
		{
			from++;
			if(NumAction<=3)/*check if it is target or source*/
			{
				nextLine[0]|= 3<<4;
				nextLine[numberOfLine]|= (command[from] - '0')<<6;
			}
			else
			{
				nextLine[0]|= 3<<2;
				nextLine[numberOfLine]|= (command[from] - '0')<<2;
			}
			numberOfLine++;
			from++;
		}
		else
			return "`Syntax error, Addressing number: 0, can't be in first addressing at this action.\0";
		break;
	}
	/*third line line*/
	if(NumAction<=3 || NumAction == 6)
	{
		from = jumpBreak(command,from);
		if(from<0)
			return "`Syntax error, expected a break ',' and another operate in this action.\0";
		from = jumpSpace(command,from);
		Addressing2 = getAddressing(command,from);
		switch(Addressing2)
		{
			case 0:
			if(NumAction == 1)
			{
				from++;
				end = 0;
				end = isNumber(command,from);
				if(end>0)/*there is a valid number between from to end*/
				{
					result = textToNum(command,from,end-1);
					if(result>128 || result<-128)/*we have only 8 bit + 2 for type of coadind*/
						return "`Syntax error, number can be between 128 to -128 in this action.\0";	
					nextLine[numberOfLine]|= ((result<<2)&(-4));
					/*int nextLine[0] in adresing we live it '0'.*/
					numberOfLine++;
					from = end;
				}
				else
					return "`Syntax error, expected a number after '#' in second operate.\0";
			}
			else
				return "`Syntax error, Addressing number: 0, can't be in second addressing at this action.\0";
			break;
			case 1:
			end = 0;
			end = endOfText(command, from);
			if(end - from >= SymbolMax)
				return "`Syntax error, too much long text afte action name. Symbol name can't be more then 30 chars.\0";
			for(i=0;i<end - from;i++)
				SyName[i] = command[from+i];
			SyName[i] = '\0';
			if((temp = GetIfExist(Head_Symbol,SyName)))
			{
				nextLine[numberOfLine]|= (temp->adress)<<2;
				if(temp->type != 2)/*meens ENTERNAL sdymbol*/
					nextLine[numberOfLine]|= 2;/*10*/
				else
				{/*meens EXTERNAL sdymbol*/
					nextLine[numberOfLine]|= 1;/*01*/
					if( addEAE(&Head_EAE, temp->name , (*IC) + numberOfLine, 1) == -2)
						return "`Dynamic allocatio error.\0";
				}				
				nextLine[0]|= 1<<2;				
				numberOfLine++;
				from = end;
			}
			else
				return "`Syntax error, Symbol tyiped in second operate dosn't exist.\0";
			break;
			case 2:/*meens THER IS a '.' */
			end = 0;
			while(command[from+end]!= '.')
				end++;		
			if(end >= SymbolMax)
				return "`Syntax error, too much long text afte break ','. Symbol name can't be more then 30 chars.\0";
			for(i=0;i<end;i++)
				SyName[i] = command[from+i];
			SyName[i] = '\0';		
			if((temp = GetIfExist(Head_Symbol,SyName)))
			{
				if(temp->type == 1 || temp->type == 2)
				{
					from += end+1;
					nextLine[numberOfLine]|= (temp->adress)<<2;
					numberOfLine++;
					if(command[from] == '1' || command[from] == '2')
						nextLine[numberOfLine]|= (command[from] - '0')<<2;
					else
						return "`Syntax error, expected 1 or 2 after: '.' in second operate.\0";
					if(temp->type != 2){/*meens ENTERNAL sdymbol*/				
						nextLine[numberOfLine-1]|= 2;/*10*/
						nextLine[numberOfLine]|= 0;/*00*/
					}
					else{				/*meens EXTERNAL sdymbol*/
						nextLine[numberOfLine-1]|= 1;/*01*/
						nextLine[numberOfLine]|= 0;/*00*/
						if( addEAE(&Head_EAE, temp->name , (*IC) + numberOfLine, 1) == -2)
							return "`Dynamic allocatio error.\0";
					}					
					nextLine[0]|= 2<<2;				
					numberOfLine++;
					from++;
				}
				else
					return "`Syntax error, expected symbol of struct.\0";
			}
			else
				return "`Syntax error, Symbol tyiped in fisrt action dosn't exist.\0";			
			break;
			case 3:/*meens command[from] = "r*..." */
			from++;
			nextLine[0]|= 3<<2;
			if(Addressing1 == 3)/*check if needed enother word*/
			{
				nextLine[numberOfLine-1]|= (command[from] - '0')<<2;
			}
			else
			{
				nextLine[numberOfLine]|= (command[from] - '0')<<2;
				numberOfLine++;
			}
			from++;
			break;
		}
	}
	else
	{
		if(isTextLeft(command,from))
			return "`Syntax error, unexpected text, after operate.\0";
	}
	if(isTextLeft(command,from))
		return "`Syntax error, unexpected text after end of command.\0";
	return addCodeToDB(nextLine,numberOfLine,IC);
}

char *entryToEAE(char *command, int from, int end)
{
	static char name[SymbolMax];
	ptSymbol temp = Head_Symbol;
	int Nlength = end - from +1,i,result;
	for(i=0;i<Nlength;i++)
	{
		name[i] = command[from+i];
	}
	name[i] = '\0';	
	while(temp)
	{		
		if(strcmp(temp->name,name) == 0)
		{			
			if(temp->type == 2)
				return "`Syntax error, entery Symbol can't be external one.\0";
			result = addEAE(&Head_EAE, temp->name, temp->adress, 0);
			if(result == -2)
				return "`Syntax error, Error in dynamic alocation.\0";
			else
				return NULL;
		}
		temp = temp->next;
	}
	return "`Syntax error, Symbol dosn't exist in hole file.\0";
}

void endSystem()
{
	deleteDataList(&Head_AsData);
	DeleteSymbols(&Head_Symbol);
	deleteListCode(&Head_Code);
	DeleteEAE(&Head_EAE);
}