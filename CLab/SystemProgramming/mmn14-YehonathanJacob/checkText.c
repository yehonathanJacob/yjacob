#include "checkText.h"
#define SymbolMax 30
/*command[from+iterator] != ':' && command[from+iterator] != '\0'*/
char *directives[5] = {"data\0","string\0","struct\0","entry\0","extern\0"};
char *orders[16] = {"mov\0","cmp\0","add\0","sub\0","not\0","clr\0","lea\0","inc\0","dec\0","jmp\0","bne\0","red\0","prn\0","jsr\0","rts\0","stop\0"};


int isSymbol(char *command, int from){
    int iterator=1;
    if (isalpha(command[from])){
        while(isalpha(command[from+iterator]) || isdigit(command[from+iterator])){
            if(iterator>SymbolMax){
                return -1;
            }
            iterator++;
        }
        if (command[from+iterator] == ':')
            return from+iterator;
    }
    return -1;
}
int isDirective (char *command, int from){
    int iterator = 1;
    char directive[7];
    int i;    
    if(command[from] == '.'){        
        while((command[from+iterator] != ' ') && (command[from+iterator] !='\t') && (command[from+iterator] !='\0')){
            if(iterator>=7)
                return -1;
            directive[iterator-1]=command[from+iterator];
            iterator++;
        }        
        directive[iterator-1]='\0';
        for (i=0;i<5;i++){
            if(strcmp(directive,directives[i])==0){
                return i+1;
            }
        }
        return -1;

    }    
    return -1;
}
int isOrder (char *command, int from){
    int iterator=0;
    char order[5];
    int i;    
    while (iterator<4 && command[from+iterator] !='\0' && !isspace(command[from+iterator])){
        order[iterator]=command[from+iterator];
        iterator++;
    }    
    order[iterator]='\0';
    for (i=0;i<16;i++){
        if(strcmp(order,orders[i])==0){
            return i;
        }
    }    
    return -1;
}

int isNumber(char *command, int from)
{
    int start = from ,end = 0;
    if(start+end < commanSize && (command[start+end] == '-' || command[start+end] == '+'))
        start++;
    while (command[start+end] != '\0' && command[start+end]>='0' && command[start+end]<='9'){        
        end++;
    }
    return (end == 0)? -1: start+end;
}