/*Functions of main file*/
char *entryToEAE(char *command, int from, int end);				/*Input: command and the start+end of symbol name. 
																 *Action: scannig Symbol list to finde this symbol, and if exist with the right consept- add it to EAE list. 
																 *Output: as string- error if exist. 
																 *Discount: (1) + All lists exist and set up.*/
int printToFile(const char *fileName);							/*Input: file name.
																 *Action: create and right the 3 output files.
																 *Output: num>0 if sucssec, or -2 if Dynamic alocation error.
																 *Discount: (1) + All lists exist and set up.*/
int dataToCode(int IC);										    /*Input: IC - last adress in code list.
																 *Action: adding data List to code.
																 *Output: num>0 if sucssec, or -2 if Dynamic alocation error.
																 *Discount: (1) + All lists exist and set up.*/
char *convertOrderToCode(int NumAction, char *command, int from,int *IC);/*Input: command and the method number. 
																 *Action: scannig the method, and add to the right lists, the correct method. 
																 *Output: as string- error if exist. 
																 *Discount: (1) + number of method is: 0-15.*/
void endSystem();												/*Action: endding all system, and deleteing lists.
																 *Discount: (1) + All lists exist and set up.*/