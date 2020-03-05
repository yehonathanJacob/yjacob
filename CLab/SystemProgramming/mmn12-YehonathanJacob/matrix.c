#include <stdio.h>
#include <stdlib.h>
#include "data.h"
extern int N;
int checkEnd();

int ** buildMatrix(int **p)
{
	int i,j,next,count = 0,num = 0;
	p = (int **)malloc(N*sizeof(int *)); /*Arry of pointers*/
	for(i = 0;i< N; i++)
	{
		*(p+i) = malloc(N*sizeof(int));/*Arry of int*/
	}
	for(i=0;i<N;i++) /*fill Matrix*/
	{
		for(j=0;j<N;j++)
		{
			next = getInt();
			if (next == -1)				
			{
				destroyMatrix(p);/*free all dinamic allocation*/
				return NULL;
			}
			++num;
			count += next - num;
			*(*(p+i)+j) = next;
		}
	}
	if(!checkEnd())
	{
		printf("Erorr: the was supos to be no more vlaue after the %dth value.\n",(N*N) );
		destroyMatrix(p);/*free all dinamic allocation*/
		return NULL;
	}
	if(count != 0)
	{
		printf("Error: There where typed a value not between 1 - N^2 or not all diffrent\n");
		destroyMatrix(p);/*free all dinamic allocation*/
		return NULL;
	}
	return p;
}
void destroyMatrix(int **p)
{
	int i;
	for(i = 0;i< N; i++)
	{
		free(*(p+i));
	}
	free(p);

}
int checkMatrix(int **p)
{
	enum { False, True};
	int status = True;
	int magicNumber = 0;
	/*run first to check what is the magic number*/
	int i,j;
	for (i = 0; i < N; ++i)
	{
		magicNumber += *(*p + i);
	}
	int leftDiagonal = 0,rightDiagonal = 0;
	int countSumRow,countSumCloumn;
	/*cher all rows cloumns and diagonals line*/
	for(i=0;i<N;i++)
	{
		leftDiagonal += *(*(p+i)+i);
		rightDiagonal += *(*(p+i)+N-i-1);
		countSumRow = 0;
		countSumCloumn = 0;
		for(j=0;j<N;j++)
		{
			countSumRow += *(*(p+i)+j);
			countSumCloumn += *(*(p+j)+i);
		}
		if(countSumRow != magicNumber)
		{
			printf("Note: the %d row sum is not %d as it supos to be.\n",i ,magicNumber);
			status = False;
		}
		if(countSumCloumn != magicNumber)
		{
			printf("Note: the %d cloumn sum is not %d as it supos to be.\n",i ,magicNumber);
			status = False;
		}
	}
	if (leftDiagonal != magicNumber)
	{
		printf("Note: the left diagonal sum is not %d as it supos to be.\n" ,magicNumber);
		status = False;
	}
	if (rightDiagonal != magicNumber)
	{
		printf("Note: the right diagonal sum is not %d as it supos to be.\n" ,magicNumber);
		status = False;
	}
	return status;
}
void printMatrix(int **p)
{
	int i,j;
	for(i=0;i<N;i++)
	{
		printf("[");
		for(j=0;j<N;j++)
		{
			printf("%4d\t",*(*(p+i)+j));
			printf((j+1 < N)? "|" : "");
		}
		printf("]\n");
	}	
}