import os

DEBUG = False

SECRET_KEY = 'CHANGEME'

LOCAL_STORAGE_DIR = 'c:\\viewer-data'

CT_SCANS_DIR = os.path.join(LOCAL_STORAGE_DIR, 'scans')
FINDINGS_DIR = os.path.join(LOCAL_STORAGE_DIR, 'findings')
WORKLISTS_DIR = os.path.join(LOCAL_STORAGE_DIR, 'worklists')
LOG_DIRECTORY = os.path.join(LOCAL_STORAGE_DIR, 'logs')
REPORTS_DIR = os.path.join(LOCAL_STORAGE_DIR, 'reports')
# COMPRESSED_VOLUMES_DIR = os.path.join(LOCAL_STORAGE_DIR, 'compressed')
UPLOAD_DIR = 'uploads'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(LOCAL_STORAGE_DIR, 'db', 'validations.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

JSON_SORT_KEYS = False
DATETIME_FORMAT = '%d/%m/%Y    %H:%M:%S'
SORT_WORKLIST_FOR_USERS = []
