#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

/*declare all function*/
#include "RBTree.h"
enum COLOR { RED, BLACK };

void freeRBNode(ptRBNode ptNode);/*Input: pointer to node. Free all dynamic allocation of node and his sons. Time complexity: O(n) Place complexity: O(1)*/
ptRBNode createNode(int x);/*Input: key of node. Output: pointer to created node. Time complexity: O(1) Place complexity: O(1)*/

ptRBNode TREE_SUCCESSOR(ptRBTree T, ptRBNode x);/*get next node in tree as sorted list (code as in page 234). Time complexity: O(log n)*/
ptRBNode TREE_PREDECESSOR(ptRBTree T, ptRBNode x);/*get prive node in tree as sorted list (code as in page 234). Time complexity: O(log n)*/
void LEFT_ROATE(ptRBTree T, ptRBNode x);/* do left roate on x in RBTree as red-black-tree (code as in page 234). Discounts: RBTree z and right[z] are defined. Time complexity: O(1)*/
void RIGHT_ROATE(ptRBTree T, ptRBNode x);/* do right roate on x in RBTree as red-black-tree (code as in page 234). Discounts: RBTree z and left[z] are defined. Time complexity: O(1)*/
void RB_INSERT_FIXUP(ptRBTree T, ptRBNode z);/* fix the color and do roates to the RBTree as red-black-tree (code as in page 236). Discounts: RBTree and z are defined. Time complexity: O(log n)*/
void RB_INSERT(ptRBTree pRB, ptRBNode z);/*insert node to RBTree as red-black-tree (code as in page 236). Discounts: RBTree and z are defined. Time complexity: O(log n)*/

void fix_Mid(ptRBTree pRB ,ptRBNode z);/*fix the mid due to the position of new z. Discounts: RBTree and z are defined. Time complexity: O(log n)*/


/* MAIN FUNCTION THAT INSERT NEW NODE */
int insertNode(ptRBTree pRB,int x)
{
	ptRBNode z;
	z = createNode(x);
	if(z)/*check if memory was successfuly created dynamic alocation*/
	{
		RB_INSERT(pRB,z);/*add node to RBTree as red-black-tree. Time complexity: O(log n)*/		
		fix_Mid(pRB, z);/*due to new z and and number of node in tree, moov the mid to it successor or predecessor. Time complexity: O(log n)*/
	}
	else
	{
		printf("Error: memory could not be allocated. \n");
		return -1;
	}
	return 1;
}


/* MAINTENANCE TREE FUNCTION */
ptRBTree createRBTree()/*Time complexity: O(1) Place complexity: O(1)*/
{
	ptRBTree pRB;
	ptRBNode nil = NULL; /*pointer to a nil node*/
	pRB = (ptRBTree)malloc(sizeof(RBTree));
	if(pRB)
	{
		nil = createNode(-1);/* in MMN16 ther is definition, that all value are between 0 and 1023*/
		if(nil)
		{
			nil->color = BLACK;/*set color of nil node*/
			pRB->root = nil;
			pRB->mid = nil;
			pRB->nil = nil;
			pRB->n = 0;
		}
		else
		{
			free(pRB);
			return NULL;
		}
	}
	return pRB;
}

ptRBNode createNode(int x)
{
	ptRBNode pNode;
	pNode = (ptRBNode)malloc(sizeof(RBNode));
	if(pNode)
	{
		/*Set all defult value of new RBNode. Color will be set later.*/
		pNode->key = x;
		pNode->parent = NULL;
		pNode->left = NULL;
		pNode->right = NULL;		
	}
	return pNode;
}

void freeRBTree(ptRBTree *pRB)/*Time complexity: O(n) Place complexity: O(n).*/
{
	if(*pRB)
	{
		freeRBNode((*pRB)->root);/*free all dynamic memori in tree, in recursion*/
		free((*pRB)->nil);
		free(*pRB);
		*pRB = NULL;
	}
}

void freeRBNode(ptRBNode ptNode)/*Travel the tree in inorder. Time complexity: O(n) Place complexity: O(n).*/
{
	if(ptNode && ptNode->key != -1)
	{
		freeRBNode(ptNode->left);
		freeRBNode(ptNode->right);
		free(ptNode);
	}
}

void fix_Mid(ptRBTree pRB ,ptRBNode z)
{
	int n = pRB->n;
	if(n == 0)/*case z is first node*/
	{
		pRB->mid = z;
		pRB->n++;
	}
	else/*meens mid is set.*/
	{
		/*option of Tree as sorted list are: (n%2 == 1) { x [mid] x } or: (n%2 == 0) { x [mid] x x } */
		if(n%2 == 1)/*meens old tree as sorted list: { x [mid] x }*/
		{
			if(((pRB->mid)->key) > (z->key))/*meens new tree as sorted List: { z x mid [x] x } -> { z [mid] x x } */
			{		
				pRB->mid = TREE_PREDECESSOR(pRB, pRB->mid);			
			}
			/*else: meens new List: { x [mid] x z } -> { x [mid] x z } NO CHANGE*/
		}
		else /*meens old list: { x [mid] x x }*/
		{			
			if(((pRB->mid)->key) <= (z->key))/*meens new List: { x [x] mid x z } -> { x x [mid] x z }*/
			{		
				pRB->mid = TREE_SUCCESSOR(pRB, pRB->mid);			
			}
			/*else: meens new List: { z x [mid] x x } -> { z x [mid] x x } NO CHANGE*/
		}
		pRB->n++;
	}
}


/* BASIC FUNCTION OF RB-TREE */
void RB_INSERT(ptRBTree pRB, ptRBNode z)
{
	ptRBNode y,x,nil;
	nil = pRB->nil;
	y = nil;
	x = pRB->root;	
	while(x != nil)
	{		
		y = x;
		if((z->key) < (x->key))
			x = x->left;
		else
			x = x->right;
	}	
	z->parent = y;	
	if(y == nil)/*case z is first value*/
		pRB->root = z;
	else/*set the parent of z*/
		if((z->key) < (y->key))
			y->left = z;
		else
			y->right = z;
	z->left = nil;
	z->right = nil;
	z->color = RED;	
	RB_INSERT_FIXUP(pRB, z);/* fix the color and do roates to the RBTree as red-black-tree */	
}

void RB_INSERT_FIXUP(ptRBTree T ,ptRBNode z) 
{
	ptRBNode y = NULL;
	while(((z->parent)->color) == RED)/*meens also that parent[p] is not nil*/
	{		
		if((z->parent) == (((z->parent)->parent)->left))
		{			
			y = ((z->parent)->parent)->right;/*set Y*/
			if((y->color) == RED)/* Case 1 */
			{				
				(z->parent)->color = BLACK;
				y->color = BLACK;
				((z->parent)->parent)->color = RED;
				z = (z->parent)->parent;
			}
			else/* Case 2 or 3 */
			{
				if(z == ((z->parent)->right))/* Case 2 */
				{					
					z = z->parent;
					LEFT_ROATE(T,z);
				}
				/* Case 3 */		
				(z->parent)->color = BLACK;
				((z->parent)->parent)->color = RED;
				RIGHT_ROATE(T,(z->parent)->parent);
			}
		}
		else
		{			
			y = ((z->parent)->parent)->left;/*set Y*/
			if((y->color) == RED)/* Case 1 */
			{				
				(z->parent)->color = BLACK;
				y->color = BLACK;
				((z->parent)->parent)->color = RED;
				z = (z->parent)->parent;
			}
			else/* Case 2 or 3 */
			{
				if(z == ((z->parent)->left))/* Case 2 */
				{					
					z = z->parent;
					RIGHT_ROATE(T,z);
				}
				/* Case 3 */	
				(z->parent)->color = BLACK;
				((z->parent)->parent)->color = RED;				
				LEFT_ROATE(T,(z->parent)->parent);
			}
		}
	}	
	(T->root)->color = BLACK;
}

void LEFT_ROATE(ptRBTree T ,ptRBNode x)
{
	ptRBNode y, nil;
	nil = T->nil;
	y = x->right;
	x->right = y->left;
	if ((y->left) != (nil))
		(y->left)->parent = x;
	y->parent = x->parent;
	if(x->parent == nil)/* case x was root */
		T->root = y;
	else/* case x was not root, meens x has a parent */
		if (x == ((x->parent)->left))/* case x was left child of his parent*/
			(x->parent)->left = y;
		else
			(x->parent)->right = y;
	y->left = x;
	x->parent = y;
}

void RIGHT_ROATE(ptRBTree T ,ptRBNode x)
{
	ptRBNode y, nil;
	nil = T->nil;
	y = x->left;
	x->left = y->right;
	if ((y->right) != (nil))
		(y->right)->parent = x;
	y->parent = x->parent;
	if(x->parent == nil)/* case x was root */
		T->root = y;
	else/* case x was not root, meens x has a parent */
		if (x == ((x->parent)->right))/* case x was right child of his parent*/
			(x->parent)->right = y;
		else
			(x->parent)->left = y;
	y->right = x;
	x->parent = y;
}

ptRBNode TREE_SUCCESSOR(ptRBTree T, ptRBNode x)
{
	ptRBNode y,nil = T->nil;
	y = nil;
	if((x->right) != nil)/*get tree minimum by going down the tree so. Time complexity: O(log n)*/
	{
		x = x->right;
		while((x->left) != nil)
			x = x->left;
		return x;
	}
	y = x->parent;
	while (y != nil && x == (y->right))/*get tree minimum by going up the tree so. Time complexity: O(log n)*/
	{
		x = y;
		y = y->parent;
	}
	return y;
}

ptRBNode TREE_PREDECESSOR(ptRBTree T, ptRBNode x)
{
	ptRBNode y,nil = T->nil;
	y = nil;
	if((x->left) != nil)/*get tree maximumm by going down the tree so. Time complexity: O(log n)*/
	{
		x = x->left;
		while((x->right) != nil)
			x = x->right;
		return x;
	}
	y = x->parent;
	while (y != nil && x == (y->left))/*get tree maximumm by going up the tree so. Time complexity: O(log n)*/
	{
		x = y;
		y = y->parent;
	}
	return y;
}

