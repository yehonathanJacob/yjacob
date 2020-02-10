#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include "RBTree.h"
#include "utils.h"
ptRBTree T = NULL;

void printMedian()/*Ouput: print median to screen. Time complexity: O(1)*/
{
	if(T)
	{
		printf("median is: %d\n", (T->mid)->key);
	}	
}

int insert(int x)/*Input: new key value. Output: status if dynamic memory was successfuly allocated. Time complexity: O(log n).*/
{
	return insertNode(T, x);
}

void MMN16(int arr[],int n1,int n2,int n3,int arrlength)
{
	int i,status;	
	T = createRBTree();
	if(T)/*only if tree was successfuly allocated so start the algorithem, and free all the memory in the end*/
	{
		status = 1;/*this flag made to check that all dynamic allocation where successfuly allocated*/
		i= 0;
		while(i<arrlength && status)/*run over the arry ones, and print median in each sellected point break.*/
		{
			status = insert(arr[i]);
			i++;
			if((i == n1 || i == n2 || i == n3) && status)/*if arive to point break, so print median*/
			{
				printf("Point break %d:\n\t",i);				
				printMedian();
			}
		}		
		freeRBTree(&T);
	}
	else
	{
		printf("Error: memory could not be allocated.\n");
	}	
}