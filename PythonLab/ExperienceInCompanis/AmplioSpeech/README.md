# AmplioSpeech Poll application
This is a Django application with SQLite DB that implement https://www.easypolls.net/
Created by Yehonathan Jacob as part of the job application process for the company.


## Table of contents
* [General info](#general-info)
* [Setup](#setup)
* [Running](#Running)
* [Uses](#Uses)


## General info
This project was created by Yehonathan in three our of work (due to ability of time).
It is currently (23/04/2021) implement only the API app of the project,
including all relevant uses for the basic need of the Poll project and test for each API.
A good part to continue from can be creating simple UI for the project,
or some more tests for API. Due to ability of time I couldn't put more effort on code design.

	
## Setup
Create a new environment with Python>=3.7 \
You can create it by [Anaconda](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands)
or by [Virtualenv](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
```
$ cd polls
$ pip install -r requirements.txt
```

## Running
To run the server, run this command from `AmplioSpeech/polls` directory: \
`python manage.py runserver`\
To stop the server just click `Crtl + C` or close the application.\
To run the tests, from the same directory run: \
`python manage.py test`\
For full API guideline you can look into the [API documentation](https://documenter.getpostman.com/view/6436758/TzJvdwWw)

## Uses
This application is implementing simple users management, 
in order to document each vote by user and blocking users to vote twice for the same poll.
- Login: http://127.0.0.1/login
- Logout:  http://127.0.0.1/logout
- Managing users: http://127.0.0.1/admin

The DB coming with the code already contain simple admin. 
To use this project you can log in as admin and change the password.\
Admin details:
- Username: `admin`
- Password: `ampliospeech`