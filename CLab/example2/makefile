myprog : prog.o utils.o
	gcc -g -ansi -Wall prog.o utils.o -o myprog
prog.o : prog.c data.h
	gcc -c -ansi -Wall prog.c -o prog.o
utils.o : utils.c
	gcc -c -ansi -Wall utils.c -o utils.o
