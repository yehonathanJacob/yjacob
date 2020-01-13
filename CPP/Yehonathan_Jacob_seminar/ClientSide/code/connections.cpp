#include "pch.h"

size_t CurlWrite_CallbackFunc_StdString(void *, size_t, size_t, string *);



 bool MyRequest::test(string host, int port) {
	MyRequest req(port, host);
	return req.myHTTPSrequets("{\"script\":[\"1+2\"]}", "test") == "true";
}


MyRequest::MyRequest(int port, string host) {
	_port = port;
	_host = host;
}

string MyRequest::compile(char * command) {
	string jsonstr = "{" + quote + "script" + quote + ":" + quote+ command+quote+"}";	
	return myHTTPSrequets(jsonstr,"compile");
}

string MyRequest::get_my_url(string api_name) {
	return  "https://" + _host + ":" + to_string(_port) + "/" + api_name;
}

string MyRequest::myHTTPSrequets(string jsonstr,string api_name)
{
	CURLcode ret;
	CURL *hnd;
	struct curl_slist *slist1;
	string data;
	slist1 = NULL;
	slist1 = curl_slist_append(slist1, "Content-Type: application/json");
	string _url = "https://" + _host + ":" + to_string(_port) + "/" + api_name;
	hnd = curl_easy_init();
	curl_easy_setopt(hnd, CURLOPT_URL, _url.c_str());	
	curl_easy_setopt(hnd, CURLOPT_NOPROGRESS, 1L);
	curl_easy_setopt(hnd, CURLOPT_POSTFIELDS, jsonstr.c_str());
	curl_easy_setopt(hnd, CURLOPT_USERAGENT, "curl/7.38.0");
	curl_easy_setopt(hnd, CURLOPT_HTTPHEADER, slist1);
	curl_easy_setopt(hnd, CURLOPT_MAXREDIRS, 50L);
	curl_easy_setopt(hnd, CURLOPT_CUSTOMREQUEST, "POST");
	curl_easy_setopt(hnd, CURLOPT_TCP_KEEPALIVE, 1L);
	curl_easy_setopt(hnd, CURLOPT_SSL_VERIFYPEER, 0L); //only for https, remove verify because need to buy an ssl license
	curl_easy_setopt(hnd, CURLOPT_SSL_VERIFYHOST, 0L); //only for https, remove verify because need to buy an ssl license
	curl_easy_setopt(hnd, CURLOPT_WRITEFUNCTION, CurlWrite_CallbackFunc_StdString);
	curl_easy_setopt(hnd, CURLOPT_WRITEDATA, &data);

	ret = curl_easy_perform(hnd);
	if (ret != CURLE_OK)
	{
		data = "Request Failed " + data;
	}
	curl_easy_cleanup(hnd);
	hnd = NULL;
	curl_slist_free_all(slist1);
	slist1 = NULL;
	return data;
}

size_t CurlWrite_CallbackFunc_StdString(void *contents, size_t size, size_t nmemb, std::string *s)
{
	try
	{
		size_t newLength = size * nmemb;
		s->append((char *)contents, newLength);
		return newLength;
	}
	catch (bad_alloc e)
	{
		//handle memory problem
		return 0;
	}
}
