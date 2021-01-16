#!/usr/bin/env bash


# create or upgrade local db
source activate aidoc-demo-viewer
python main.py host=0.0.0.0
source deactivate aidoc-demo-viewer