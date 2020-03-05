#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "mat.h"
#include "input.h"
enum {OUT, IN};
int flag;
pmat matArr[6];

int m_read_mat();
int m_print_mat();
int m_add_mat();
int m_sub_mat();
int m_mul_mat();
int m_mul_scalar();
int m_trans_mat();
int m_stop();
int m_else();

int getMatNumber(char *);
int getMat();

int main()
{
	int i,j, funcnmber;
	char *buffer = NULL;
	char *functionName[8] = {"read_mat", "print_mat", "add_mat", "sub_mat", "mul_mat", "mul_scalar", "trans_mat", "stop"};
	int (*function[9])() = {m_read_mat, m_print_mat, m_add_mat, m_sub_mat, m_mul_mat, m_mul_scalar, m_trans_mat, m_stop, m_else};
	/*create all mat*/
	for(i= 0; i < 6; i += 1)
	{
		matArr[i] = create_mat();
		if(!matArr[i])
		{
			printf("Unable to create all 6 mat.\n");
			for(j=0;j <i; j+=1)
			{
				delete_mat(matArr[j]);
			}
			exit(0);
		}
	}

	flag = IN;
	while(flag)
	{
		printf("$:");
		buffer = getStr();
		if(buffer)/*input = "..***..."  buffer = "***" */
		{
			funcnmber = 8;
			for(i = 0;i<8;i+=1)
			{
				if(strcmp(buffer, functionName[i]) == 0)
				{
					funcnmber = i;
				}
			}
			if(function[funcnmber]())/*if was an error in one function, so check EOF*/
			{
				if(checkend())
				{
					printf("Error(1): Unexpected end of program.\n");
					m_stop();
				}
				else
				{
					runToEnd();
				}				

			}					
			free(buffer);
		}
		else/*input = "...\n or EOF..."*/
		{
			if(checkend())
			{
				printf("Error(2): Unexpected end of program.\n");
				m_stop();
			}else{
				printf("Error(3): Expected next function name.\n");
				runToEnd();
			}
		}
	}
	return 0;
}

int getMatNumber(char *string)
{
	int i = 0;
	char *mat[6] = {"MAT_A", "MAT_B", "MAT_C", "MAT_D", "MAT_E", "MAT_F"};
	for(i = 0;i<6;i +=1)
	{
		if(strcmp(mat[i],string) == 0)
			return i;
	}
	return -1;
}
int getMat()
{
	char *buffer = NULL;
	int matNumber;
	buffer = getStr();
	if(buffer)
	{
		if((matNumber = getMatNumber(buffer)) != -1)
		{
			return matNumber;
		}
		else
		{
			printf("Error(4): One or more of matrix name was undefined\n");
			return -1;
		}
		free(buffer);
	}
	else
	{
		printf("Error(5): Expected matrix name.\n");
		return -1;
	}
}

int m_read_mat()
{
	int i = 0,status;
	int p1;
	double arr[16], *next;	
	next = NULL;
	if((p1 = getMat()) != -1)
	{
		while(jumpStep() && i<16)
		{				
			if((next = getNumer()))
			{
				arr[i] = *next;
				i++;
				free(next);
			}
			else
			{
				printf("Error(6): Expected number after ','\n");				
				return 1;
			}
		}
		status = runToEnd();
		if(i >= 16 || status)
		{
			read_mat(matArr[p1], arr,i);
		}
		else
		{
			printf("Error(6.1): Unexpected value in end of command\n");			
		}		
				
	}
	else
	{
		return 1;
	}
	return 0;
}

int m_print_mat()
{		
	int p1;
	if((p1 = getMat()) != -1)
	{
		if(runToEnd())
		{
			print_mat(matArr[p1]);
		}
		else
		{
			printf("Error(8): Unexpected char in the end of command.\n");
		}
	}
	else
	{
		return 1;
	}
	return 0;
}

int m_add_mat()
{		
	int p1, p2, p3;
	if((p1 = getMat()) != -1)
	{
		if(jumpStep() && (p2 = getMat()) != -1 && jumpStep())
		{
			if((p3=getMat()) != -1)
			{
				if(runToEnd())
				{					
					add_mat(matArr[p1],matArr[p2],&matArr[p3]);					
				}
				else
				{
					printf("Error(9): Unexpected char in the end of command.\n");
				}
			}
			else { return 1;}			
		}
		else
		{
			printf("Error(10): Missing parameter\n");		
			return 1;
		}
	}
	else { return 1;}
	return 0;
}

int m_sub_mat()
{	
	int p1, p2, p3;
	if((p1 = getMat()) != -1)
	{
		if(jumpStep() && (p2 = getMat()) != -1 && jumpStep())
		{
			if((p3=getMat()) != -1)
			{
				if(runToEnd())
				{
					sub_mat(matArr[p1],matArr[p2],&matArr[p3]);
				}
				else
				{
					printf("Error(11): Unexpected char in the end of command.\n");
				}
			}
			else { return 1;}			
		}
		else
		{
			printf("Error(12): Missing parameter\n");		
			return 1;
		}
	}
	else { return 1;}
	return 0;
}

int m_mul_mat()
{	
	int p1, p2, p3;
	if((p1 = getMat()) != -1)
	{
		if(jumpStep() && (p2 = getMat()) != -1 && jumpStep())
		{
			if((p3 = getMat()) != -1)
			{
				if(runToEnd())
				{
					mul_mat(matArr[p1],matArr[p2],&matArr[p3]);
				}
				else
				{
					printf("Error(13): Unexpected char in the end of command.\n");
				}
			}
			else { return 1;}			
		}
		else
		{
			printf("Error(14): Missing parameter\n");		
			return 1;
		}
	}
	else { return 1;}
	return 0;
}

int m_mul_scalar()
{	
	int p1, p2;
	double *next= NULL;
	if((p1 = getMat()) != -1)
	{
		if(jumpStep())
		{
			if((next = getNumer()))
			{
				if(jumpStep())
				{
					if((p2 = getMat()) != -1)
					{
						if(runToEnd())
						{
							mul_scalar(matArr[p1], *next,&matArr[p2]);
						}
						else
						{
							printf("Error(13): Unexpected char in the end of command.\n");
						}						
					}
					else { free(next); return 1;}
				}
				else
				{
					printf("Error(15): Missing parameter\n");
					free(next);
					return 1;
				}
				free(next);
			}
			else
			{
				printf("Error(16): Expected number\n");		
				return 1;
			}
		}
		else
		{
			printf("Error(17): Missing parameter\n");		
			return 1;
		}
	}
	else { return 1;}
	return 0;
}
int m_trans_mat()
{	
	int p1, p2;
	if((p1 = getMat()) != -1)
	{
		if(jumpStep())
		{
			
			if((p2 = getMat()) != -1)
			{
				if(runToEnd())
				{
					trans_mat(matArr[p1], &matArr[p2]);
				}
				else
				{
					printf("Error(13): Unexpected char in the end of command.\n");
				}				
			}
			else { return 1;}		
		}
		else
		{
			printf("Error(18): Missing ',' and then parameter\n");		
			return 1;
		}
	}
	else { return 1;}
	return 0;
}

int m_stop()
{
	int i;
	for(i = 0;i<6;i+=1)
	{
		delete_mat(matArr[i]);
	}
	flag = OUT;
	runToEnd();
	return 0;
}

int m_else()
{
	printf("Error(19): Unknown command name\n");
	runToEnd();
	return 0;
}