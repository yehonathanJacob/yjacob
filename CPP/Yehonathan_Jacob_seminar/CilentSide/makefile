Client : oFiles/main.o oFiles/inputs.o oFiles/connections.o
	g++ -g -Wall oFiles/main.o oFiles/inputs.o oFiles/connections.o -o Client
oFiles/main.o : cppFiles/main.cpp cppFiles/main.h cppFiles/inputs.h cppFiles/connections.h
	g++ -c -ansi -Wall cppFiles/main.cpp -o oFiles/main.o
oFiles/inputs.o : cppFiles/inputs.cpp cppFiles/inputs.h
	g++ -c -ansi -Wall cppFiles/inputs.cpp -o oFiles/inputs.o
oFiles/connections.o : cppFiles/connections.cpp cppFiles/connections.h
	g++ -c -ansi -Wall cppFiles/connections.cpp -o oFiles/connections.o