int my_strcmp(char str1[], char str2[])
{
	int i=0;
	while(str1[i] && str2[i] && (str1[i] == str2[i]))
	{
		++i;	
	}
	/*End of comperation, cheking the last i*/
	if(!str1[i] && !str2[i])
		return 0;
	if(str1[i] > str2[i])
		return 1;
	else
		return -1;
}
int my_strncmp(char str1[], char str2[], int size)
{
	int i=0;
	while(str1[i] && str2[i] && (str1[i] == str2[i]) && i<size)
	{
		++i;	
	}
	/*End of comperation, cheking the last i*/
	if((!str1[i] && !str2[i]) || i == size)
		return 0;
	if(str1[i] > str2[i])
		return 1;
	else
		return -1;
}
int my_strchr(char str[], char c)
{
	int i=0;
	while(str[i] && str[i] != c)
	{
		++i;
	}
	/*End of comperation, cheking the last i*/
	if(str[i] == c)
		return i;
	else
		return -1;
}