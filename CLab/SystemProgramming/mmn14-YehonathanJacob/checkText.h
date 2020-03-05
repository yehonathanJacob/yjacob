#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "AsInput.h"


int isSymbol(char *command, int from);/* input: char array which represents a string, and an integer 'from'
                                       * output: an integer
                                       * action: if starting from the index 'from', there is a label (as described in the book) in the string, return the index of the end of the label, else return -1 */

int isDirective (char *command, int from);/* input: char array which represents a string, and an integer 'from'
                                           * output: an integer
                                           * action: if starting from the index 'from', there is a directive (as described in the book) in the string, return the index of the directive by the bool, else return -1 */

int isOrder (char *command, int from);/* input: char array which represents a string, and an integer 'from'
                                           * output: an integer
                                           * action: if starting from the index 'from', there is an order (as described in the book) in the string, return the index of the order by the bool, else return -1 */

int isNumber(char *command, int from);/* input: char array which represents a string, and an integer 'from'
                                           * output: an integer, index after the number or -1 otherwise.
                                           * action: if starting from the index 'from', there is a number in the string, return the index of the end of the number, else return -1 */
