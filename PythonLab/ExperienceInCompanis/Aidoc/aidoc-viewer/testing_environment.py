import os
import argparse

from flask import send_from_directory, render_template
from flask_login import login_required
from flask_login import current_user

from utils.testing_envitonment.init_app import app
from utils.testing_envitonment.login_api import login_urls, login_manager
from utils.testing_envitonment.search_api import search_urls
from utils.testing_envitonment.data_api import data_urls

BASE_URL = app.config.get('BASE_URL_TEST', '/test')

login_manager.init_app(app)
app.register_blueprint(login_urls, url_prefix=f'{BASE_URL}/login')
app.register_blueprint(data_urls, url_prefix=f'{BASE_URL}/data')
app.register_blueprint(search_urls, url_prefix=f'{BASE_URL}/search')


@app.route(f'{BASE_URL}/static/<path:path>')
def send_static(path):
    static_dir = os.path.join(os.path.abspath(os.getcwd()), 'static')
    return send_from_directory(static_dir, path)


@app.route(f'{BASE_URL}')
@login_required
def index():
    return render_template('testing_UI/main_testing_page.html', username=current_user.username, base_url = BASE_URL)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='127.0.0.1', type=str)
    parser.add_argument('--port', default='1234', type=str)
    args = parser.parse_args()

    app.run(port=args.port, host=args.host)
