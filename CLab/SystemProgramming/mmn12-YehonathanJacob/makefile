magic : magic.o matrix.o input.o
	gcc -g -ansi -Wall -pedantic magic.o matrix.o input.o -o magic
magic.o : magic.c data.h
	gcc -c -ansi -Wall magic.c -o magic.o
matrix.o : matrix.c data.h
	gcc -c -ansi -Wall matrix.c -o matrix.o
input.o : input.c data.h
	gcc -c -ansi -Wall input.c -o input.o