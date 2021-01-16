# aidoc-viewer

aidoc-viewer aka Validation Platform is the platform used mostly to demo the aidoc
prediction algorithms results.


c cds

1. Python 3

https://www.python.org/downloads/

2. Conda

https://conda.io/docs/user-guide/install/


Install dev environment
============================

```bash
git clone https://bitbucket.org/aidoc/aidoc-viewer
cd <install-dir>/aidoc-viewer
conda env create -f environment.yml
source activate aidoc-demo-viewer
```


PyCharm IDE
=============================

To edit the code in PyCharm:

Create New Project in PyCharm in aidoc-viewer 

add conda env to pycharm in __Preferences -> Project Interpreter__


Download Input Data
=============================

Create a directory in your home dir for the data files.

```bash
mkdir ~/viewer-data
```

Download all the directories from the following link (it might take a couple of minutes):


https://www.dropbox.com/sh/e7znqpfupgioyww/AACHyLnOh8k7bdJvaifTEWp6a?dl=0

to the __viewer-data__ directory 


Configure the code to use the data files:

```bash
mkdir instance
cp config.py instance/
```

Change the paths in __instance/config.py__ to point to you data files. You should have something like this:

```python

CT_SCANS_DIR = os.path.join(os.path.expanduser('~'), 'viewer-data', 'scans')
FINDINGS_DIR = os.path.join(os.path.expanduser('~'), 'viewer-data', 'findings')
WORKLISTS_DIR = os.path.join(os.path.expanduser('~'), 'viewer-data', 'worklists')

```

Create Database:
==================================
```bash
python manage.py db upgrade
```


Start the webserver
======================================
Run 
```bash
python main.py 
```

Alternatively you can run main.py in PyCharm

Load data

```bash
curl 'http://localhost:5000/api/admin/load-data'
```

You should get:
```bash
{
  "status": "Success"
}
```


Now go to your favorite browser and type:

http://localhost:5000

You should get a login page!

use demo/d123456 to login




