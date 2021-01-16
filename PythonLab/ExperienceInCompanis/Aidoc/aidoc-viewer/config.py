import os

DEBUG = False
SECRET_KEY = 'CHANGEME'
DB_NAME = 'validations.db'
APPLICATION_INSIGHTS_INSTRUMENTATION_KEY = ''

MOUNTED_DATA_DRIVE = os.path.join(os.path.sep, 'mnt', 'datadrive')
LOCAL_DATA_DRIVE = os.path.join(os.path.sep, 'datadrive', 'viewer-data')

CT_SCANS_DIR = os.path.join(MOUNTED_DATA_DRIVE, 'scans')
REPORTS_DIR = os.path.join(MOUNTED_DATA_DRIVE, 'reports')
FINDINGS_DIR = os.path.join(MOUNTED_DATA_DRIVE, 'findings')
WORKLISTS_DIR = os.path.join(MOUNTED_DATA_DRIVE, 'worklists')

LOG_DIRECTORY = os.path.join(LOCAL_DATA_DRIVE, 'logs')
LOCAL_DB_DIR = os.path.join(LOCAL_DATA_DRIVE, 'db-data')
COMPRESSED_VOLUMES_DIR = os.path.join(LOCAL_DATA_DRIVE, 'compressed-scans')

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(LOCAL_DB_DIR, DB_NAME)

UPLOAD_DIR = 'uploads'

BONE_WINDOW = [300, 1500]
WIDE_BONE_WINDOW = [700, 3200]
BODY_WINDOW = [40, 400]
AP_WINDOW = [2048, 2048]
BRAIN_HYPERDENSE_WINDOW = [35, 80]
LUNG_WINDOW = [-400, 1500]
DEFAULT_WINDOW_DEFS = {
    'brain': BRAIN_HYPERDENSE_WINDOW,
    'cspine': BONE_WINDOW,
    'tspine': BONE_WINDOW,
    'lspine': BONE_WINDOW,
    'thorax': LUNG_WINDOW,
    'chest': LUNG_WINDOW,
    'abdomen': BODY_WINDOW,
    'pe': BODY_WINDOW,
    'cta_head': BODY_WINDOW,
    'xray_ap': AP_WINDOW,
    'xray_ap_ngt':[2249,3262],
    'xray_ap_tld':[1881, 2777],
    'xray_ap_pneumothorax': [1717, 2666],
    'skull': WIDE_BONE_WINDOW,
    'chest_vascular': BODY_WINDOW,
    'bone_lesion': BONE_WINDOW,
    'abdomen_pelvis': BODY_WINDOW,
    'chest_bone': BONE_WINDOW,
    'brain_vo': BODY_WINDOW,
    'chest_abdomen_pelvis_bone': BONE_WINDOW,
    'chest_abdomen_pelvis_ah': [-19,492],
    'chest_abdomen_pelvis_body': BODY_WINDOW,
    'xray_hip': AP_WINDOW,
    'xray_foot': [1530,3444],
}

JSON_SORT_KEYS = False
DATETIME_FORMAT = '%d/%m/%Y    %H:%M:%S'
SORT_WORKLIST_FOR_USERS = []
