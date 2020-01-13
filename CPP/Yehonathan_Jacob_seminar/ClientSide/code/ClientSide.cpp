// ClientSide.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include "pch.h"
#include <iostream>


int main()
{
	Inputs in;
	string host;
	int port;
	cout << "------------------------------------------------" << endl;
	cout << "This C++ application compile Python3 script (as Python Shell)" << endl;
	cout << "------------------------------------------------" << endl;
	do {
		cout << "PLEASE CHECK OUT SERVER IS ON" << endl;
		host = in.get_host();
		port = in.get_port();
	} while (! MyRequest::test(host, port));
	
	MyRequest req(port, host);
	cout << "------------------------------------------------" <<endl;
	cout << "CONNECTED TO:" << req.get_my_url() << endl<<endl;
	printf("Please enter Python command (max %d char per line).\nType 'safe_functions()' for knowing witch function you are aloowd to use.\nType 'exit' for finish this session\n", bufSize);
	cout << "------------------------------------------------" << endl;
	string buffer_data = "exit";
	cout << "> ";
	while (in.is_more()) {
		char *buf = new char[bufSize];
		if (!in.get_command(buf)) {
			cout << "> ";
			continue;
		}
		buffer_data = string(buf);
		int a = buffer_data.find("exit");
		if (buffer_data.find("exit") == 0)
			break;		
		string result = req.compile(buf);
		cout << result;
		cout << "> ";
	}

	return 0;
}