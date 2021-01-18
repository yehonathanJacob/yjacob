import json
from app.init_app import config

def get_data():
    path_to_data = config.DATA_JSON_PATH
    with open(path_to_data, 'r') as file:
        data = json.load(file)
    return data