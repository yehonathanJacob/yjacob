int getAddressing(char *command, int from);								/*Input: command and index to start from.																			
																			* Output: adrressing number (0-3).																		
																			*/

char * countActionList (int actionNum, int *L, char *command, int from); /*Input: action number, pointer to L, command and index to start from.
																			* Discounts: (1) and, actionNumber is correct (0-15)
																			* Output: set L to number of nedded words in code file, and NULL if ther is NO ERROR
																			*/
char *adressOfSymbol(char *command, int from, int end, ptSymbol head); /*Input: action number, pointer to L, command and index to start from.
																			* Discounts: (1) and, actionNumber is correct
																			* Output: set L to number of nedded words in code file, and NULL if ther is NO ERROR
																			*/