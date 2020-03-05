mymat : mymat.o mat.o input.o
	gcc -g -ansi -Wall -pedantic mymat.o mat.o input.o -o mymat
mymat.o : mymat.c mat.h input.h
	gcc -c -ansi -Wall -pedantic mymat.c -o mymat.o
mat.o : mat.c input.h
	gcc -c -ansi -Wall -pedantic mat.c -o mat.o
input.o : input.c
	gcc -c -ansi -Wall -pedantic input.c -o input.o