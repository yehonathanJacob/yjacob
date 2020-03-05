#include <stdio.h>
#include <ctype.h>

#define OUT 0
#define IN 1
int main()
{
	int state = -1; /*Not OUT because then we need '\n' betweem them*/
	int stateQuote = OUT;
	int c;/*char, in int because it can get EOF>char*/
	while ((c = getchar()) != EOF)
	{
		if(c < '0' || c > '9') /*Is not a digit*/
		{			
			if(state < IN)/*meens that state is OUT or didn't start even*/
			{
				if(!isspace(c)) /*Is not a white char - we are starting new sentence*/
				{
					if(state == OUT) {putchar('\n');}
					if(c == '"')
					{
						stateQuote = IN;
						putchar('"');
					}
					else /*Is not a '"'*/
					{						
						putchar(toupper(c));
					}
					state = IN; /*Is IN now.*/
				}
			}
			else/*we are in a sentence*/
			{
				if(c == '"')
				{
					stateQuote = (stateQuote == IN)? OUT:IN;
					putchar('"');
				}
				else
				{
					if(stateQuote == IN)
					{
						putchar(toupper(c));
					}
					else
					{
						putchar(tolower(c));
					}
				}
			}

			if (c == '.' && stateQuote == OUT)/*After char was added, now check if it was the end of a sentence*/
			{
				putchar('\n');
				state = OUT;
			}
			
		}
	}
	return 1;
}