FROM ubuntu:18.04

RUN apt-get update && \
    apt-get -y install python3.7 && \
    apt-get -y install python3-pip

COPY . /opt/source-code

# Setup DB:
RUN cd /opt/source-code/ && \
    pip3 install -r requirements.txt && \
    cd /opt/source-code/assiment2 && \
    python3 setup_db.py


RUN apt-get update && \
    apt-get install -y wget xvfb unzip curl
# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# set display port to avoid crash
ENV DISPLAY=:99

# install selenium
RUN pip3 install selenium==3.8.0

ENV CHROMEDRIVER_DIR /usr/local/bin/
WORKDIR /opt/source-code

CMD ["/opt/source-code/assiment2/web_service.py"]
ENTRYPOINT ["python3"]



