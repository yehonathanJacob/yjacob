#include <stdio.h>
#include "data.h"
#define MAX_N 99

int N;

int main()
{	
	int **p = NULL;
	if((N = getInt()) && N <= MAX_N && N>=3)
	{
		if((p = buildMatrix(p)) != NULL)
		{
			/*N was decleard, and matrix was biuld.*/
			printf("The matrix size is %dX%d \n", N,N);
			printf("The matrix coatain: \n");
			printMatrix(p);
			printf("check if matrix is magic square:\n");
			if(checkMatrix(p))
			{
				printf("True: matrix is magic square\n");
			}
			else
			{
				printf("False: matrix is NOT magic square\n");
			}
			destroyMatrix(p);/*free all dinamic allocation*/
		}
		else
		{
			printf("Error in biulding matrix.\n");
		}		
	}
	else if(N != -1)
	{
		printf("N is Not in the right range (3 <= N <= %d)\n",MAX_N);
	}	
	return 0;
}