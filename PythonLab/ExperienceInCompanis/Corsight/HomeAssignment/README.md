# Yehonathan Jacob home assignment to Corsight
This home assignment made by Yehonathan Jacob as part of his audition to Corsight.

## Table of contents
#### Uses
* [Setup](#Setup)
* [Running](#Running)
#### Documentation
* [PART 1 create matching process](#part-1)
    - [SourceReader module](#SourceReader)
    - [ParallelMatching module](#Parallel)
* [PART 2 creating WebServer](#part-2)
* [Tests](#tests)
<a id="Setup" name="setup"></a>
## Setup
Create a new environment with Python>=3.7 \
You can create it by [Anaconda](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands)
```
$ conda env create -f environment.yml
```
or by [Virtualenv](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
```
$ pip install -r requirements.txt
```
From now on I will consider as if you are running for the dedicated environment.

<a id="Running" name="Running"></a>
## Running
There rae few entrypoint.  
Each and everyone has a unitest and can be run by simply running the tests.
The framework is `pytest` and can be test by running the next command
from the root of the project (by the project environment)
```
$ pytest
```
To run the web server which is implemented in `FastAPI` 
can be done by running the next command from root directory:
```
$ python WebServer/main.py
```


<a id="part-1" name="part-1"></a>
## Part 1 - create matching process
There are two modules: the `ParallelMatching` which has the main class as requested 
by the task, and the `SourceReader` which is made to control the reading
and the iteration on the data.
To go directly to the requested method in the task you can go to 
the [run_parallel_matching](#run_parallel_matching) class method. 

<a id="SourceReader" name="SourceReader"></a>
#### SourceReader
The `SourceReader` module contain in the `basic_reader.py` file
the `BasicSource` class which is the interface of the readers classes.
Each reader contain a source path, which is basically a path to file unless the child
handle the raised error and having a directory of path.
In the `sources.py` file there are two classes:
- `PandasReader` which made to read CSV files, using pandas. 
  (This mean all the file is getting read). If I had more time I would implement
  another reader that will read only one value at a time.
- `DirectoryReader` which is made to read full paths of all the files
    there is in a given directory.

<a id="Parallel" name="Parallel"></a>
#### ParallelMatching
The `ParallelMatching` module contain in the `parallel_matching.py` file
Has two classes. The `Match` class which simulate a single match, contain the source file, and the number of intersection founded.
The second and major class is: `ParallelMatching` class, which made to compare two directories.
Therefore it's instance contain path to directory A, path to directory B and number of minimum intersections. \
There are two main entrypoint in there:
- `load_matches_results` which parallel iterate over the files directories in path A, and multiporcessly start to iterate over
the directories in path B to find the highest match score.
  Eventually this function return a list of all matches with the heights score.
- <a id="run_parallel_matching" name="run_parallel_matching"></a>`run_parallel_matching` class method that gets all four
parameters: A, B, C and X. Then it load the matches results list, and in multithreading
  start to copy each file in the match results, then eventually write to the 
  `scores.txt` all the scores.



<a id="part-2" name="part-2"></a>
## Part 2 - creating web server
There is a basic web server created in the file `main.py`
using the framework of `FastAPI`. To run the server there is a need reset the `Directories` class
for letting the API work with it. By running the `main.py`, there will be a use of temporary directory
for that. Which will be release by the end of the process.
In the test of this webserver, each test implement and setup its own temporary directory.\
When the web server is running, you can go to http://localhost:8000/ to see the documents of the API.


<a id="tests" name="tests"></a>
## Tests
Under the `test` directory there are test files for each module in the project (including the web server)
made by `pytest`.\
Of course I couldn't implement all needed test, but I made the best in this short time.

