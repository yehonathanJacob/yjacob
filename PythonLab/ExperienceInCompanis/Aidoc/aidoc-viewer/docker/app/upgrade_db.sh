#!/usr/bin/env bash

source activate aidoc-demo-viewer
python manage.py db upgrade
source deactivate aidoc-demo-viewer