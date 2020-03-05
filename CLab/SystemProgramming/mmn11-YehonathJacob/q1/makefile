my_string : my_string.o function.o
	gcc -g -ansi -Wall -pedantic my_string.o function.o -o my_string
my_string.o : my_string.c data.h
	gcc -c -ansi -Wall -pedantic my_string.c -o my_string.o
function.o : function.c
	gcc -c -ansi -Wall -pedantic function.c -o function.o