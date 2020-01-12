// Tips for Getting Started: 
//   1. Use the Solution Explorer window to add/manage files
//   2. Use the Team Explorer window to connect to source control
//   3. Use the Output window to see build output and other messages
//   4. Use the Error List window to view errors
//   5. Go to Project > Add New Item to create new code files, or Project > Add Existing Item to add existing code files to the project
//   6. In the future, to open this project again, go to File > Open > Project and select the .sln file

#ifndef PCH_H
#define PCH_H
#include <iostream>
#include <string>
#include <stdio.h>
#include <list> 
#include <iterator> 

#include <curl/curl.h>

#include "connections.h"
#include "inStream.h"

using namespace std;

#define bufSize 100
#define hostSize 50
#define portSize 5
#define defaultPort 8443
#define defaultHost "localhost"


// TODO: add headers that you want to pre-compile here

#endif //PCH_H
