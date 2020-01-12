#include "pch.h"
#include <string>
using namespace std;

class MyRequest
{
public:
	MyRequest(int port, string host);
	string compile(char * command);
	string myHTTPSrequets(string jsonstr, string api_name);
	string get_my_url(string api_name = "");
	static bool test(string host, int port);
private:
	string _host;
	int _port;
	string quote = "\"";
};
