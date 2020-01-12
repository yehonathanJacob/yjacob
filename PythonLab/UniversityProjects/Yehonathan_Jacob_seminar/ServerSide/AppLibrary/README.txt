I have created the SSL certification for free with the help of this turial:
https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https
and with runnig this coammand in linux enviroment:
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365