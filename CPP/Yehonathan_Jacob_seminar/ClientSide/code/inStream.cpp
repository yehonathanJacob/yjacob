#include "pch.h"


Inputs::Inputs() {
	canGo = true;
	first = EOF;
}
bool Inputs::is_more() {
	if (canGo) //check next char only if can go
	{
		first = getchar();
		canGo = first != EOF;
	}
	return canGo;
}

bool Inputs::get_command(char buf[]) {	
	if (!canGo || first=='\n')
		return false;
	buf[0] = first;
	cin.getline((&(buf[1])), bufSize - 1);
	return true;
}

string Inputs::get_host() {
	printf("Please type the server host (default %s): ", defaultHost);
	string host;
	if (is_more() && first != '\n') {
		char *buf = new char[hostSize];
		buf[0] = first;
		cin.getline((&(buf[1])), hostSize - 1);
		host = string(buf);
	}
	else {
		host = defaultHost;
	}
	if (host == "\n")
		host = defaultHost;
	canGo = true;
	return host;
}
int Inputs::get_port() {
	printf("Please type the server port (default %d): ", defaultPort);
	int port;
	if (is_more() && first != '\n') {
		port = -1;
		do {
			try {
				char *buf = new char[portSize];
				buf[0] = first;
				cin.getline((&(buf[1])), portSize - 1);
				string s_port = string(buf);
				if (s_port != "\n")
					port = stoi(s_port);
				else
					port = defaultPort;
			}
			catch (const std::invalid_argument)
			{
				port = -1;
				printf("Please type the server port (default %d): ", defaultPort);
			}
		} while (port == -1 && is_more());
		if (port == -1) //case we arive to EOF without port
			port = defaultPort;
	}
	else {
		port = defaultPort;
	}
	canGo = true;
	return port;
}