import os, sys
import logging

from flask import Flask

ROOT_PATH = os.getcwd()
sys.path.append(ROOT_PATH)
logging.getLogger().setLevel(logging.DEBUG)
template_folder=os.path.join(ROOT_PATH, 'templates')
static_folder=os.path.join(ROOT_PATH, 'static')

app = Flask(__name__, static_url_path='', instance_relative_config=True, template_folder=template_folder, static_folder=static_folder)

if os.path.isdir(app.config.root_path):
    from instance import config
else:
    logging.warning('Cannot find instance directory - using default configuration')
    from app import default_config as config

logging.info(f'implementing app for URL: {config.BASE_URL}')

