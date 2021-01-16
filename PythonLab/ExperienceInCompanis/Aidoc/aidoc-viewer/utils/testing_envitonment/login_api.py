import flask
from flask import Blueprint, request, render_template
from flask_login import LoginManager
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required

from models import models

from utils.DbLoader import dbLoader
from sqlalchemy.orm.exc import NoResultFound

login_manager = LoginManager()
login_manager.login_view = "/test/login/view"

login_urls = Blueprint('login_urls', __name__)

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(user_id)


@login_urls.route('/view', methods=['GET', 'POST'])
def login():
    return render_template('testing_UI/login_testing.html')


@login_urls.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    next = flask.request.args.get('next')
    return flask.redirect(next or flask.url_for('index'))


@login_urls.route('/login', methods=['POST', 'GET'])
def login_auth():
    login_data = request.args.to_dict()
    try:
        user = dbLoader.login_user(login_data)

        if user.username != 'admin':
            return render_template('testing_UI/login_testing.html', message='Only admin can log in')

        if user.password != login_data['password']:
            return render_template('testing_UI/login_testing.html', message='Invalid password')

        login_user(user)

        flask.flash('Logged in successfully.')
        next = flask.request.args.get('next')

        return flask.redirect(next or flask.url_for('index'))

    except NoResultFound:
        return render_template('testing_UI/login_testing.html', message='Invalid username')
