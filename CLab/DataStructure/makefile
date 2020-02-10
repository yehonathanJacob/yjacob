mmn16 : main.o RBTree.o utils.o
	gcc -g -ansi -Wall main.o RBTree.o utils.o -o mmn16
main.o : main.c utils.h
	gcc -c -ansi -Wall main.c -o main.o
utils.o : utils.c utils.h RBTree.h
	gcc -c -ansi -Wall utils.c -o utils.o
RBTree.o : RBTree.c RBTree.h
	gcc -c -ansi -Wall RBTree.c -o RBTree.o
