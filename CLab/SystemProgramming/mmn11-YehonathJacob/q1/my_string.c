#include <stdio.h>
#include "data.h"

int my_strcmp(char[], char[]);
int my_strncmp(char[], char[],int);
int my_strchr(char[], char);

int main()
{
	int selection = 0;
	char str1[maxSizeOfArr];
	char str2[maxSizeOfArr];
	char c;
	int size;
	printf("\nPlease select a function:");
	printf("\n (1) For my_strcmp(str1,str2)");
	printf("\n (2) For my_strncmp(str1,str2)");
	printf("\n (3) For my_strchr(str1,str2)");
	printf("\nYour selection: ");
	scanf("%d",&selection);
	switch(selection)
	{
		case 1: /*my_strcmp function:*/
			printf("\nmy_strcmp function:");
			printf("\nType string to the first str: ");
			scanf("%s",str1);
			printf("Type string to the second str: ");
			scanf("%s",str2);
			printf("\nThe result is: %d\n",my_strcmp(str1, str2));
			break;		
		case 2: /*my_strncmp function:*/
			printf("\nmy_strncmp function:");
			printf("\nType string to the first str: ");
			scanf("%s",str1);
			printf("Type string to the second str: ");
			scanf("%s",str2);
			printf("Type the maximum number of characters to be compared: ");
			scanf("%d",&size);
			printf("\nThe result is: %d\n",my_strncmp(str1, str2, size));
			break;
		case 3:	/*my_strchr function:*/
			printf("\nmy_strchr function:");
			printf("\nType string to the str: ");
			scanf("%s",str1);
			printf("Type char to get index of: ");
			scanf(" %c", &c);
			printf("\nThe result is: %d\n",my_strchr(str1, c));
			break;
		default:/*non of the above function:*/
			printf("\nYour selection didn\'t feet to any of our function.\n");
			break;
	}
	return 1;
}