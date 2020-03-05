#include "Code.h"

int isEmptyCode(codePointer head){
    if(head==NULL)
        return 1;
    return -1;
}

int addCode(codePointer * head ,int address ,char *bin) {
    codePointer newData = (codePointer) malloc(sizeof(codeNode));
    codePointer temp;
    if (newData == NULL) {
        return -2;
    }
    newData->address = address;
    newData->bin = bin;    
    newData->next = NULL;
    if (isEmptyCode(*head)>0) {

        *head = newData;
        return 1;
    }

    temp = *head;
    while (temp->next != NULL) {
        temp = temp->next;
    }
    temp->next = newData;
    return 1;


}

codePointer getNextCode(codePointer current){
    return current->next;
}

char * getCode(codePointer * head){
    char * converted=(char *)malloc(6*sizeof(char));
    codePointer temp=*head;
    char * charTemp;
    if(!converted)
        return NULL;
    (*head)=(*head)->next;
    memcpy(converted,decimalToMozar((temp)->address),2);
    converted[2]='\t';
    charTemp = converted+3;
    memcpy(charTemp,binToMozar((temp)->bin),2);
    converted[5]='\0';
    return converted;
}

void deleteListCode(codePointer * head){
    codePointer pt,temp;
	temp = *head;
	while(temp)
	{
		pt = temp->next;		
        free(temp->bin);
		free(temp);
		temp = pt;
	}
	*head = NULL;
}
