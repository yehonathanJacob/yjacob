#include <stdio.h>
#include "data.h"

int find_big(int, int);

int main()
{
	int x,y;
	printf("\nType %d numbers\n",counter);
	printf("x: ");
	scanf("%d",&x);
	printf("y: ");
	scanf("%d",&y);
	/*scanf("%d:%d",&x,&y);*/
	printf("\nThe sum of %d and %d is %d\n",x,y,x+y);
	printf("\nThe biggest number is: %d\n",find_big(x,y));
	return 0;
}
