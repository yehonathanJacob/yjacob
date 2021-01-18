import argparse
import logging

from flask import send_from_directory, render_template

from app.init_app import app, config
from utils.utils import get_data

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html', BASE_URL=config.BASE_URL)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    logging.info(f"Starting server at: {config.BASE_URL}")
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
