typedef struct RBTree * ptRBTree;
typedef struct RBNode * ptRBNode;
typedef struct RBTree{ 
	ptRBNode root; /*pointer to head of RBTree*/
	ptRBNode mid; /*pointer to head of middel node*/
	ptRBNode nil; /*pointer to a nil node*/
	int n; /*number of values in RBTree*/
}RBTree;
typedef struct RBNode{
	int key; /*key of value*/
	ptRBNode parent;/*pointer to parent*/
	ptRBNode left;/*pointer to left node in RB-Tree*/
	ptRBNode right;/*pointer to right node in RB-Tree*/	
	short color; /*color in RB-Tree (0 or 1)*/
}RBNode;
ptRBTree createRBTree(); /*Output: pointer to new RBTree. Time complexity: O(1)*/

int insertNode(ptRBTree pTL,int x);/*Input: RBTree and Key of new node. Discounts: RBTree is defined.*/

void freeRBTree(ptRBTree *pTL); /*Input: pointer to RBTree. Delete and free all dynamic alocation*/