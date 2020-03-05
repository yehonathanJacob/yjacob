#include <stdio.h>
#include <stdlib.h>
#include "mat.h"
#include "input.h"
#define MAT_SIZE 4
enum boolean {OUT,IN};
typedef struct mat
{
	double **index;
}mat;

static void setInMat(pmat p,int i, int j,double number) 
{ 
	*(*((p->index)+i)+j) = number; 
}
static double getFromMat(pmat p,int i, int j) 
{ 
	return *(*((p->index)+i)+j);
}


pmat create_mat()
{
	pmat newPmat;
	int i,j;	
	newPmat = (pmat)malloc(sizeof(mat));
	if(newPmat)
	{
		newPmat->index = (double **)malloc(MAT_SIZE*(sizeof(double *)));
		if(newPmat->index)
		{
			for(i=0; i<MAT_SIZE; i+=1)
			{
				*((newPmat->index)+i) = (double *)malloc(MAT_SIZE*(sizeof(double)));
				if(!(*((newPmat->index)+i)))/*case one of malloc didn't success*/
				{
					for(j = 0;j<=i;j+=1)
					{
						free(*((newPmat->index)+j));
					}
					return NULL;
				}
			}
		}else{
			free(newPmat);
			return NULL;
		}
	}else{
		return NULL;
	}	
	return newPmat;
}

void delete_mat(pmat p)
{
	int i;
	for(i=0;i<MAT_SIZE;i+=1)
	{
		free(*((p->index)+i));
	}
	free(p);
}

void read_mat(pmat p, double *arr, int Last)
{
	int i,j,k=0;
	for(i = 0;i <MAT_SIZE; i+=1)
	{
		for(j = 0;j<MAT_SIZE; j+=1)
		{
			if(Last >= k)
			{
				setInMat(p,i,j,arr[k]);
				k++;
			}
			else
			{
				setInMat(p,i,j,0);
			}
		}
	}
}

void print_mat(pmat p)
{	
	int i,j;
	printf("\n");
	for(i=0; i < MAT_SIZE; i=i+1)
	{
		printf("[");
		for(j=0; j < MAT_SIZE; j= j+1)
		{
			printf("%9.2f",getFromMat(p,i,j));
			printf((j+1 < MAT_SIZE)? "|" : "");
		}
		printf("]\n");
	}
}

void add_mat(pmat p1,pmat p2,pmat *p3)
{
	int i,j;
	double number;
	
	pmat newPmat = create_mat();
	if(newPmat)
	{
		for(i=0; i < MAT_SIZE; i=i+1)
		{		
			for(j=0; j < MAT_SIZE; j= j+1)
			{
				number = getFromMat(p1,i,j) + getFromMat(p2,i,j);
				setInMat(newPmat,i,j,number);
			}		
		}		
		delete_mat(*p3);		
		*p3 = newPmat;
				
	}
	else
	{
		printf("Error(23): can't create in storeg new matrix for result\n");
	}
}

void sub_mat(pmat p1,pmat p2,pmat *p3)
{
	int i,j;
	double number;
	pmat newPmat = create_mat();
	if(newPmat)
	{
		for(i=0; i < MAT_SIZE; i=i+1)
		{		
			for(j=0; j < MAT_SIZE; j= j+1)
			{
				number = getFromMat(p1,i,j) - getFromMat(p2,i,j);
				setInMat(newPmat,i,j,number);
			}		
		}
		delete_mat(*p3);
		*p3 = newPmat;
	}
	else
	{
		printf("Error(24): can't create in storeg new matrix for result\n");
	}
}
void mul_mat(pmat p1,pmat p2,pmat *p3)
{
	int i,j,k;
	double number;
	pmat newPmat = create_mat();
	if(newPmat)
	{
		for(i=0; i < MAT_SIZE; i=i+1)
		{		
			for(j=0; j < MAT_SIZE; j= j+1)
			{
				number = 0;
				for(k=0; k < MAT_SIZE; k= k+1)
				{
					number += getFromMat(p1,i,k) * getFromMat(p2,k,j);
				}				
				setInMat(newPmat,i,j,number);
			}		
		}
		delete_mat(*p3);
		*p3 = newPmat;
	}
	else
	{
		printf("Error(25): can't create in storeg new matrix for result\n");
	}
}

void mul_scalar(pmat p1,double d,pmat *p2)
{
	int i,j;
	double number;
	pmat newPmat = create_mat();
	if(newPmat)
	{
		for(i=0; i < MAT_SIZE; i=i+1)
		{		
			for(j=0; j < MAT_SIZE; j= j+1)
			{
				number = getFromMat(p1,i,j) * d;
				setInMat(newPmat,i,j,number);
			}		
		}
		delete_mat(*p2);
		*p2 = newPmat;
	}
	else
	{
		printf("Error(26): can't create in storeg new matrix for result\n");
	}
}
void trans_mat(pmat p1,pmat *p2)
{
	int i,j;
	double number;
	pmat newPmat = create_mat();
	if(newPmat)
	{
		for(i=0; i < MAT_SIZE; i=i+1)
		{		
			for(j=0; j < MAT_SIZE; j= j+1)
			{
				number = getFromMat(p1,i,j);
				setInMat(newPmat,j,i,number);
			}		
		}
		delete_mat(*p2);
		*p2 = newPmat;
	}
	else
	{
		printf("Error(27): can't create in storeg new matrix for result\n");
	}
}