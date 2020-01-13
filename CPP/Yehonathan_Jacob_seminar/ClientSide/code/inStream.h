#include "pch.h"
using namespace std;

class Inputs
{
public:
	Inputs();
	bool get_command(char buf[]);
	bool is_more();
	string get_host();
	int get_port();
private:
	char first;
	bool canGo;
};
