#include "AsData.h"

int addNumber(char * command, int iterator, int endNum, int *DC, dataPointer * head);/*adds the number in command that is represented as a string from index 'iterator' to index 'endNum'. returns (1) above.*/

int addStringThatIsNotADirective(char * command,int from,dataPointer * head,int * DC); /*Receives as an input a char array command, which in its index from there is the beginning of a string ("), and adds it to the dataList.returns the position after the second quotation marks if succeeded,-2 if there was an error in dynamic allocation and -1 otherwise*/

int addNumber(char * command, int iterator, int endNum, int *DC, dataPointer * head){
    int newNumber = textToNum(command,iterator,endNum);        
    int added;
    if(newNumber>512 || newNumber<-512)
        return -1;
    if ((added = addNode(head, newNumber, DC) < 0))
        return added;
    return 1;
}

int addNode(dataPointer *head , int number, int *DC){
    dataPointer newData = (dataPointer)malloc(sizeof(dataList));
    dataPointer temp;
    if(newData == NULL){
        return -2;
    }
    newData->data=number;
    newData->DC=*DC;
    newData->next=NULL;
    *DC+=1;
    if(*head==NULL){
        *head=newData;
        return 1;
    }

    temp=*head;
    while(temp->next!=NULL){
        temp=temp->next;
    }
    temp->next=newData;
    return 1;

}
int addStringThatIsNotADirective(char * command,int from,dataPointer * head,int * DC){
    int iterator=from;
    int added;
    if(command[iterator]!='\"')
        return -1;
    iterator++;
    while(command[iterator]!='\"' && isTextLeft(command,iterator)) {
        if ((added = addNode(head, command[iterator], DC)) < 0)
            return added;
        iterator++;
    }
    if(command[iterator] != '\"')
        return -1;
    if((added = addNode(head,'\0',DC))<0)
        return added;
    return iterator+1;
}
int addString(char *command, int from, int *DC, dataPointer *head){
    int iterator=from+stringSize;    
    iterator=jumpSpace(command,iterator);
    return addStringThatIsNotADirective(command,iterator,head,DC);
}

int addStruct(char *command, int from, int *DC, dataPointer *head) {
    int iterator = from+structSize;
    int endNum;
    int num;
    int endStruct;    
    iterator = jumpSpace(command, iterator);
    if ((endNum = isNumber(command, iterator)) < 0) {
        return -1;
    }    
    num = addNumber(command,iterator,endNum-1,DC,head);
    if(num<0)
        return num;
    iterator=endNum;
    iterator=jumpSpace(command,iterator);
    if(command[iterator]!=',')
        return -1;
    iterator=jumpSpace(command,iterator+1);
    if(command[iterator]!='\"')
        return -1;
    if((endStruct=addStringThatIsNotADirective(command,iterator,head,DC))<0)
        return endStruct;    
    return endStruct;
}

int addData(char *command, int from, int *DC, dataPointer*head){
    int iterator=from+dataSize;
    int endNum;
    int number;    
    iterator=jumpSpace(command,iterator);
    if(!isTextLeft(command,iterator))
        return -1;
    if((endNum = isNumber(command,iterator))<0)
        return endNum;    

    number=addNumber(command,iterator,endNum-1,DC,head);
    if(number<0)
        return number;
    iterator=endNum;    
    while(isTextLeft(command,iterator)) {
        iterator=jumpSpace(command,iterator);
        if(command[iterator]!=',')
            return iterator;
        iterator=jumpSpace(command,iterator+1);
        if((endNum = isNumber(command,iterator))<0)
            return endNum;        
        number=addNumber(command,iterator,endNum-1,DC,head);
        if(number<0)
            return number;
        iterator=endNum;        
    }
    return iterator;
}

void deleteDataList(dataPointer * head){    
    dataPointer pt,temp;
    temp = *head;
    while(temp)
    {
        pt = temp->next;        
        free(temp);
        temp = pt;
    }
    *head = NULL;
}

void printDataList(dataPointer head){
    dataPointer temp = head;
    while(temp){
        printf("(%d,%d)\n",temp->data,temp->DC);
        temp=temp->next;
    }
}
