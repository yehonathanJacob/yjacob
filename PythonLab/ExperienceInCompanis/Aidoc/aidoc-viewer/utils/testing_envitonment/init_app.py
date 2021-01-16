import os
import logging

from flask import Flask

from utils.DbLoader import dbLoader
from utils.scan_compression import ScanCompressor
from utils.db import db
from utils.encoder import NumpyNumberEncoder
from utils.app_insights_client import app_insights_client

static_dir = os.path.join(os.path.abspath(os.getcwd()),'static')
template_dir = os.path.join(static_dir, 'templates')
app = Flask(__name__, static_url_path='', instance_relative_config=True, template_folder=template_dir)
app.config.from_object('config')
if os.path.isdir(app.config.root_path):
    app.config.from_pyfile('config.py')
else:
    logging.warning('Cannot find instance directory - using default configuration')

app.json_encoder = NumpyNumberEncoder
app.secret_key = app.config.get('SECRET_KEY')

db.init_app(app)

app_insights_client.init_app(app.config.get('APPLICATION_INSIGHTS_INSTRUMENTATION_KEY'))

db_loader_logger = logging
if not app.debug:
    from logging.handlers import RotatingFileHandler

    formatter = logging.Formatter("[%(asctime)s] {%(module)s:%(lineno)d} %(levelname)s - %(message)s")
    log_dir = app.config.get('LOG_DIRECTORY', '.')
    os.makedirs(log_dir, exist_ok=True)
    logfile = os.path.join(log_dir, 'aidoc-viewer.log')
    file_handler = RotatingFileHandler(logfile, maxBytes=5 * 1024 * 1024, backupCount=10)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    log = logging.getLogger('werkzeug')
    log.setLevel(logging.INFO)

    logging.root.setLevel(logging.INFO)
    logging.root.addHandler(file_handler)

    db_loader_logger = app.logger
else:
    logging.root.setLevel(logging.DEBUG)
    app.logger.setLevel(logging.DEBUG)

db_loader_logger.info('Using worklists dir: %s', app.config['WORKLISTS_DIR'])
db_loader_logger.info('Using findings dir: %s', app.config['FINDINGS_DIR'])
db_loader_logger.info('Using CT scans dir: %s', app.config['CT_SCANS_DIR'])
db_loader_logger.info('Using compressed volumes dir: %s',
                      app.config['COMPRESSED_VOLUMES_DIR'] or app.config['CT_SCANS_DIR'])

scan_compressor = ScanCompressor(app.config['CT_SCANS_DIR'], app.config['COMPRESSED_VOLUMES_DIR'])

dbLoader.init(app.config['WORKLISTS_DIR'], app.config['FINDINGS_DIR'], app.config['CT_SCANS_DIR'],
              scan_compressor, logger=db_loader_logger)
