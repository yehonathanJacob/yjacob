# Yehonathan Jacob home assignment to Reigoinv
This home assignment made by Yehonathan Jacob as part of his audition to Reigoinv.

## Table of contents
#### Uses
* [Setup](#Setup)
* [Running](#Running)
#### Documentation
* [ASSIGNMENT 1 liner_regression_sum](#part-1)
* [ASSIGNMENT 2 WebCrawling](#part-2)

<a id="Setup" name="setup"></a>
## Setup
- Setup python environment:\
  Create a new environment with Python>=3.7 \
  You can create it by [Anaconda](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands)
  ```
  $ conda env create -f environment.yml
  ```
  or by [Virtualenv](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
  ```
  $ pip install -r requirements.txt
  ```
  From now on I will consider as if you are running for the dedicated environment.\
- Setup chromedriver:\
  This project is arriving with chromedriver version 81 (the version that compatible with my Chrome). \
  If this driver doesn't fit your system, you will get error with the version you need to download:\
  ``Current browser version is YOUR_CHROME_VESION with binary path /usr/bin/google-chrome``\
  To download dedicated driver, goto [chromedriver/downloads](https://chromedriver.chromium.org/downloads)
  download the version as appear in the error, and paste it under path: ``home_exam/assiment2/driver``
- Setup DB:\
  goto `/home_exam/assiment2/` and run
  ```
  $ python setup_db.py
  ```
  
  

<a id="Running" name="Running"></a>
## Running
All runnig are from ``/home_exam`` path with the dedicated environment.
- To run the test:\
  ```
  $ pytest -s
  ```
- To run the web server which is implemented in `FastAPI`:
  ```
  $ python WebServer/main.py
  ```


<a id="part-1" name="part-1"></a>
## ASSIGNMENT 1 liner_regression_sum
The liner regression is implemented with numpy in the file liner_regression_sum.py

<a id="part-2" name="part-2"></a>
## ASSIGNMENT 2 WebCrawling
The crawler implemented with selenium in the file crawler.py
The process is happening in the instance of ZillowCrawler under the method crawle_apartment_details(address)
There is end to end test in the file test_crawler which could be great entry point.
Everytime you run the crawler there is a test to see if there is reCHAPCHA to pass.\
If so, and error is getting rasied and you (as a user) will be require to pass it.
This is why we run the test with `-s` flag, to enable user intersection.
The DB is implemented in the file database_manager.py with SQLAlchemy.
The DB is getting setup in the file setup_db.py with SQLite so after the setup
you should see a file named pythonsqlite.db
The webserver is implemented in the file web_server.py with FastAPI