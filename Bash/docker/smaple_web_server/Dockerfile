FROM ubuntu:18.04

RUN apt-get update
RUN apt-get -y install python3.7
RUN apt-get -y install python3-pip

RUN pip3 install flask

COPY . /opt/source-code

CMD ["/opt/source-code/app.py"]
ENTRYPOINT ["python3"]