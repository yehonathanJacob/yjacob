assembler : main.o AsInput.o AsSymbol.o extAndEnt.o Code.o checkText.o convertText.o AsData.o action.o utils.o
	gcc -g -ansi -Wall -pedantic main.o AsInput.o AsSymbol.o extAndEnt.o Code.o checkText.o convertText.o AsData.o action.o utils.o -o assembler
main.o : main.c AsInput.h AsSymbol.h extAndEnt.h Code.h checkText.h convertText.h AsData.h action.h utils.h
	gcc -c -ansi -Wall -pedantic main.c -o main.o
AsInput.o: AsInput.c AsInput.h
	gcc -c -ansi -Wall -pedantic AsInput.c -o AsInput.o
AsSymbol.o : AsSymbol.c AsSymbol.h AsInput.h
	gcc -c -ansi -Wall -pedantic AsSymbol.c -o AsSymbol.o
extAndEnt.o: extAndEnt.c 
	gcc -c -ansi -Wall -pedantic extAndEnt.c -o extAndEnt.o
checkText.o: checkText.c checkText.h
	gcc -c -ansi -Wall -pedantic checkText.c -o checkText.o
Code.o: Code.c convertText.h
	gcc -c -ansi -Wall -pedantic Code.c -o Code.o
convertText.o: convertText.c convertText.h
	gcc -c -ansi -Wall -pedantic convertText.c -o convertText.o
AsData.o: AsData.c AsData.h convertText.h checkText.h AsInput.h
	gcc -c -ansi -Wall -pedantic AsData.c -o AsData.o
action.o: action.c action.h checkText.h AsInput.h AsSymbol.h convertText.h
	gcc -c -ansi -Wall -pedantic action.c -o action.o
utils.o: utils.c AsInput.h AsSymbol.h extAndEnt.h Code.h checkText.h convertText.h AsData.h action.h utils.h
	gcc -c -ansi -Wall -pedantic utils.c -o utils.o