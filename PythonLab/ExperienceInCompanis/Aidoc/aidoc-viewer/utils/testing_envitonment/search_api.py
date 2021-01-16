# import os
# import argparse
# import logging
#
# import flask
from flask import Flask, request, send_from_directory, abort, render_template, Blueprint
# from flask_login import LoginManager
# from flask_login import login_user
from flask_login import login_required
from flask_login import current_user
# from flask_login import logout_user
from flask.json import jsonify
# from werkzeug.datastructures import Headers
from sqlalchemy.orm.exc import NoResultFound

from scan import Scan
from models import models
# from utils.DbLoader import dbLoader
# from utils.scan_compression import ScanCompressor
# from utils.db import db
# from utils.encoder import NumpyNumberEncoder
# from utils import reports
from utils.testing_envitonment.init_app import app

search_urls = Blueprint('search_urls', __name__)

@search_urls.route('/worklist', methods=['POST', 'GET'])
@login_required
def search_user_worklist():
    if not current_user.is_admin:
        abort(403)

    sub_username = request.args.get('search', '')
    try:
        users = models.User.query.filter(models.User.username.contains(sub_username)).all()

        usernames = [{'text': user.username, 'id': user.id} for user in users]
        usernames = [{'text': "All", 'id': -1}] + usernames

        return jsonify(usernames)
    except NoResultFound:
        app.logger.warning('Work list not found for user: %s', current_user.username)
        return jsonify([])


@search_urls.route('/study', methods=['POST', 'GET'])
@login_required
def search_user_study():
    if not current_user.is_admin:
        abort(403)

    sub_stduy_uid = request.args.get('search', '')
    user_id = int(request.args.get('user_id') or -1)
    series_id = int(request.args.get('series_id') or -1)

    try:

        study_uids_query = models.WorkItem.query.filter(models.WorkItem.uid.contains(sub_stduy_uid))
        if user_id != -1:
            study_uids_query = study_uids_query.filter(models.WorkItem.user_id.is_(user_id))

        if series_id != -1:
            series = models.Series.query.filter(models.Series.id.is_(series_id)).one()
            study_uids_query = study_uids_query.filter(models.WorkItem.id.is_(series.work_item_id))

        study_uids = study_uids_query.all()
        worklist = [{'text': work_item.uid, 'id': work_item.id} for work_item in study_uids]
        worklist.append(no_selection_option())

        return jsonify(worklist)
    except NoResultFound:
        app.logger.warning('Work list not found for study uid: %s', sub_stduy_uid)
        return jsonify([])


@search_urls.route('/series', methods=['POST', 'GET'])
@login_required
def search_user_series():
    if not current_user.is_admin:
        abort(403)

    sub_series_uid = request.args.get('search', '')
    work_item_id = int(request.args.get('work_item_id') or -1)

    try:

        series_uids_query = models.Series.query.filter(models.Series.uid.contains(sub_series_uid))
        if work_item_id != -1:
            series_uids_query = series_uids_query.filter(models.Series.work_item_id.is_(work_item_id))

        series_uids = series_uids_query.all()
        series_ls = [{'text': series.uid, 'id': series.id} for series in series_uids]
        series_ls.append(no_selection_option())

        return jsonify(series_ls)
    except NoResultFound:
        app.logger.warning('series not found for sub series uid: %s', sub_series_uid)
        return jsonify([])


@search_urls.route('/slice', methods=['POST', 'GET'])
@login_required
def search_user_slice():
    if not current_user.is_admin:
        abort(403)

    sub_slice_num = request.args.get('search', '')
    series_id = int(request.args.get('series_id') or -1)

    if series_id == -1:
        return jsonify([])

    try:

        series_uids_query = models.Series.query.filter(models.Series.id.is_(series_id))
        series = series_uids_query.one()

        scan = Scan.fromID(series.uid, app.config['CT_SCANS_DIR'], read_volume=False)

        number_of_slices = scan.size[0]

        slices = [{'text': str(i), 'id': i} for i in range(1, number_of_slices + 1) if sub_slice_num in str(i)]

        return jsonify(slices)
    except NoResultFound:
        app.logger.warning('slice not found for series uid: %s', series_id)
        return jsonify([])

def no_selection_option():
    return {'text': 'No selection', 'id': ''}