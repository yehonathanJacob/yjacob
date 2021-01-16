import os

from flask import Blueprint, request, abort, jsonify
from flask_login import current_user
from flask_login import login_required

from models import models
from utils.db import db
from utils.DbLoader import dbLoader


users = Blueprint('users', __name__)
_mail_sender = None


def init_users_resources(mail_sender):
    global _mail_sender
    _mail_sender = mail_sender


# prefix /api/admin/users


@users.route('/')
@login_required
def admin_get_users():
    if not current_user.is_admin:
        abort(403)
    return jsonify([user.to_json_dict() for user in models.User.query.all()])


@users.route('/roles')
@login_required
def admin_get_roles():
    if not current_user.is_admin:
        abort(403)

    return jsonify(['user', 'admin', 'study-user'])


@users.route('/add-user', methods=['POST'])
@login_required
def admin_add_user():
    if not current_user.is_admin:
        abort(403)

    user_data = request.get_json()
    username = user_data['username']

    if not username:
        return jsonify({'error': 'Username can not be empty'}), 404
    user = db.session.query(models.User).filter_by(username=username).first()
    if user:
        return jsonify({'error': 'Username: {} already exists'.format(username)}), 409

    user_res = dbLoader.create_new_user(user_data)
    return jsonify(user_res)

    
@users.route('/external-add-user-and-load-data', methods=['POST'])
def _external_admin_add_user_and_load_data():
    user_data = request.get_json()
    if user_data.get('username') != 'admin':
        abort(403)

    admin = db.session.query(models.User).filter_by(username=user_data['username']).first()
    if not admin:
        return jsonify(dict(error='No admin user found!')), 404
    if not admin.password == user_data.get('password'):
        return jsonify(dict(error='Invalid credentials')), 401

    if not user_data.get('new_user_name'):
        return jsonify(dict(error='Missing required parameter: new_user_name')), 400

    new_user_name = user_data.get('new_user_name')
    user = db.session.query(models.User).filter_by(username=new_user_name).first()
    if user:
        return jsonify(dict(error='Username: {} already exists'.format(new_user_name))), 409

    new_user_dict = dbLoader.create_new_user({
        'username': new_user_name,
        'name': user_data.get('name'),
        'email': user_data.get('email'),
        'loadFindingFiles': user_data.get('loadFindingFiles')
    })

    worklist_file = os.path.join(dbLoader.worklist_dir, new_user_dict.get('username'))
    if worklist_file:
        report = dbLoader.load_user(new_user_dict.get('username'), new_user_dict.get('name'), worklist_file)

    _mail_sender.send_new_user_credentials_and_report_email(new_user_dict, report)

    return jsonify(new_user_dict)


@users.route('/exists/<username>', methods=['POST'])
def exists(username):
    user_data = request.get_json()
    if user_data['username'] != 'admin':
        abort(403)
    admin = db.session.query(models.User).filter_by(username=user_data['username']).first()
    if not admin:
        return jsonify(dict(error='No admin user found!')), 404
    if not admin.password == user_data['password']:
        return jsonify(dict(error='Invalid credentials')), 401

    user = db.session.query(models.User).filter_by(username=username).first()
    return jsonify({'exists': bool(user)})


@users.route('/remove-user', methods=['POST'])
@login_required
def admin_remove_user():
    if not current_user.is_admin:
        abort(403)

    user_data = request.get_json()

    username = user_data['username']

    if username is None or len(username) == 0:
        return jsonify(dict(error='Username can not be empty')), 404

    user = dbLoader.get_user(username)

    if user:
        user_res = dbLoader.delete_user(user)
        return jsonify(user_res)
    else:
        return jsonify(dict(error='Username ' + username + ' already exists')), 409
