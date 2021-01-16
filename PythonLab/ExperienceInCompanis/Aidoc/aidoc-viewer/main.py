import sys
import os.path
from itertools import groupby
from flask import Flask, request, send_from_directory
from flask import abort
from flask_login import LoginManager
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from flask.json import jsonify
import numpy as np
import json
import logging
import atexit
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.datastructures import Headers

from utils.db import db
from models import models
from utils.DbLoader import dbLoader
from utils.scan_compression import ScanCompressor
from scan import Scan
from utils.encoder import NumpyNumberEncoder
from utils.MailSender import MailSender
from utils.stats import calculate_stats

from utils.UserDataUploader import UserDataUploader

from blueprints.Findings import findings
from blueprints.Users import users, init_users_resources

from utils.autodoc import auto
from utils.app_insights_client import app_insights_client
from utils import reports

app = Flask(__name__, instance_relative_config=True)
auto.init_app(app)

app.config.from_object('config')

if os.path.isdir(app.config.root_path):
    app.config.from_pyfile('config.py')
else:
    logging.warning('Cannot find instance directory - using default configuration')

app.json_encoder = NumpyNumberEncoder
app.secret_key = app.config.get('SECRET_KEY')

db.init_app(app)

app_insights_client.init_app(app.config.get('APPLICATION_INSIGHTS_INSTRUMENTATION_KEY'))

# Initialize logging system
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

mail_sender = MailSender(app.config.get('SENDGRID_API_KEY', ''), app.config.get('ADMIN_EMAIL_LIST', []))
mail_sender.init()

init_users_resources(mail_sender)

login_manager = LoginManager()
login_manager.init_app(app)

userDataUploader = UserDataUploader(app.config['UPLOAD_DIR'])
app.register_blueprint(findings, url_prefix='/api/admin/findings')
app.register_blueprint(users, url_prefix='/api/admin/users')


@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(user_id)

@app.route('/api/admin/load-all-users-to-db')
def init_db():
    '''Loads viewer data of all users from files to DB (does not overwrite, this can only be done on a per user basis using the function below)'''
    load_data_report = dbLoader.load_data()
    return jsonify({'status': 'Success', 'report': load_data_report})

@auto.doc()
@app.route('/api/admin/load-user-to-db/<username>')
@login_required
def load_data_for_user(username, delete_user_metadata_before_loading=False, overwrite_volumes=False,
                       overwrite_existing_findings_metadata=False):
    '''Loads given user viewer data from files to DB (for overwriting existing data [metadata\findings\volumes],
    see functions below). Should be used when some of the worklist items\findings\volumes aren't appearing
    '''
    if username != current_user.username and not current_user.is_admin:
        abort(403)

    worklist_file = os.path.join(dbLoader.worklist_dir, username)
    if worklist_file:
        # Initialize the data in the DB
        report = dbLoader.load_user(username, username, worklist_file,
                                    delete_user_metadata_before_loading=delete_user_metadata_before_loading,
                                    overwrite_volumes=overwrite_volumes,
                                    overwrite_existing_findings_metadata=overwrite_existing_findings_metadata)
        return jsonify(report)
    else:
        return jsonify(dict(error='Username ' + username + ' doesn\'t exists')), 500


@auto.doc()
@app.route('/api/admin/reload-user-metadata-to-db/<username>')
@login_required
def reload_user_metadata_to_db(username):
    '''IRREVERSIBLE - Deletes all the user metadata (including findings) from the DB.
    Then - performs load-user-to-db.
    (same as re-uploading the worklist with marking V on overwrite)'''
    return load_data_for_user(username, delete_user_metadata_before_loading=True, overwrite_volumes=False,
                              overwrite_existing_findings_metadata=True)

@auto.doc()
@app.route('/api/admin/reload-volumes-and-user-metadata-to-db/<username>')
@login_required
def reload_volumes_and_user_metadata_to_db(username):
    '''IRREVERSIBLE - Same as reload-user-metadata-to-db, in addition - reload volume data from raw data file to
    compressed file (otherwise the volume used will be the first volume loaded for the scan even if overwritten in the storage'''
    return load_data_for_user(username, delete_user_metadata_before_loading=True, overwrite_volumes=True,
                              overwrite_existing_findings_metadata=True)


@auto.doc()
@app.route('/api/admin/reload-user-findings-to-db/<username>')
@login_required
def reload_findings_metadata_to_db(username):
    '''IRREVERSIBLE - Deletes user findings from the db (doesnt delete the rest of the metadata), and reloads
    them from files'''
    return load_data_for_user(username, delete_user_metadata_before_loading=False, overwrite_volumes=False,
                              overwrite_existing_findings_metadata=True)


# should be changed to  post once available in the ui
@auto.doc()
@app.route('/api/admin/delete-work-item/<username>/<study_uid>', methods=['GET'])
@login_required
def delete_work_item(username, study_uid):
    '''IRREVERSIBLE - Delete a single worklist item (and all of its metadata for this current user) from the DB
    (doesnt affect other users which use this study)'''
    if username != current_user.username and not current_user.is_admin:
        abort(403)

    user = dbLoader.get_user(username)

    if user:
        for wi in user.worklist:
            if wi.uid == study_uid:
                dbLoader.delete_work_item(wi)
                return jsonify({'status': 'Success'})

        return jsonify(dict(error='Study uid ' + study_uid + ' doesn\'t  exist for user "' + username + '"')), 500
    else:
        return jsonify(dict(error='Username ' + username + ' doesn\'t exists')), 500


@app.route('/auth/login', methods=['POST'])
def login():
    login_data = request.get_json()
    try:
        user = dbLoader.login_user(login_data)

        if user.password == login_data['password']:
            login_user(user)

            ignored_users = app.config.get('IGNORED_USERS', [])

            if user.username not in ignored_users:
                mail_sender.send_login_email(user)

            return jsonify(user.to_json_dict())
        else:
            return jsonify(dict(error='Invalid username or password')), 401
    except NoResultFound:
        return jsonify(dict(error='Invalid username or password')), 401


@app.route('/auth/currentUser')
@login_required
def get_current_user():
    return jsonify(current_user.to_json_dict())


@app.route('/auth/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'success': True})


@app.route('/api/worklist')
@login_required
def get_worklist():
    try:
        worklist = [dict(item.to_json_dict(), numFindings=len(item.findings))
                    for item in current_user.worklist]
        worklist.sort(key=lambda item: item['order_by'] if item['order_by'] else 1)
        if 'SORT_WORKLIST_FOR_USERS' in app.config and current_user.username in app.config['SORT_WORKLIST_FOR_USERS']:
            # positive findings first then order by patient name
            worklist.sort(key=lambda item: (item['numFindings'] == 0, item['patientName']))

        return jsonify(worklist)
    except NoResultFound:
        app.logger.warning('Work list not found for user: %s', current_user.username)
        return jsonify([])


@app.route('/api/admin/worklist/<username>')
@login_required
def get_user_worklist(username):
    if username != current_user.username and not current_user.is_admin:
        abort(403)
    try:
        user = db.session.query(models.User).filter_by(username=username).first()

        worklist = [dict(item.to_json_dict(), numFindings=len(item.findings))
                    for item in user.worklist]

        return jsonify(worklist)
    except NoResultFound:
        app.logger.warning('Work list not found for user: %s', current_user.username)
        return jsonify([])


@app.route('/api/worklist/<uid>')
@login_required
def get_work_item_json(uid):
    try:
        work_item_json = get_work_item(uid)
        return jsonify(work_item_json.to_json_dict())
    except NoResultFound:
        app.logger.debug('Work item with uid %s not found for user %s', uid, current_user.username)
        abort(404)


@app.route('/api/worklist/<uid>', methods=['PUT'])
@login_required
def update_worklist(uid):
    try:
        work_item_json = request.get_json()
        work_item = get_work_item(uid)

        if 'status' in work_item_json:
            work_item.status = work_item_json['status']

        if 'finalized_as' in work_item_json:
            work_item.finalized_as = work_item_json['finalized_as']

        if 'favorite' in work_item_json:
            work_item.favorite = work_item_json['favorite']

        db.session.commit()

        metric_dict = work_item.to_json_dict()
        metric_dict['username'] = current_user.username

        app_insights_client.track_metric('change-status', 1, properties=metric_dict)
        return jsonify(work_item.to_json_dict())
    except NoResultFound:
        app.logger.warning('Work item with uid %s not found for user: %s', uid, current_user.username)
        abort(404)


@app.route('/api/worklist/<uid>/reset', methods=['PUT'])
@login_required
def reset_work_item(uid):
    ''' IRREVERSIBLE - Deletes user-added-findings (my findings) and sets all other findings (aidoc findings)
    to default state (pristine without additional details)
    '''
    try:
        work_item = get_work_item(uid)
        work_item.status = 'pending'

        models.Finding.query.filter_by(
            work_item_id=work_item.id, status='new'
        ).delete()

        db.session.execute('UPDATE ' + models.Finding.__tablename__ + ' ' +
                           "SET status = 'pristine', comment = NULL, locations = original_locations " +
                           'WHERE work_item_id = ' + str(work_item.id) + " AND status <> 'pristine'")

        db.session.commit()

        metric_dict = work_item.to_json_dict()
        metric_dict['status'] = 'reset'
        metric_dict['username'] = current_user.username

        app_insights_client.track_metric('change-status', 1, properties=metric_dict)

        return jsonify(dict(work_item.to_json_dict(),
                            findings=[x.to_json_dict() for x in work_item.findings]))
    except NoResultFound:
        app.logger.warning('Work list with uid %s not found for user: %s', uid, current_user.username)
        abort(404)

@auto.doc()
@app.route('/api/studies/<username>')
@login_required
def get_studies(username):
    '''Returns studies details for given user'''
    if username != current_user.username and not current_user.is_admin:
        abort(403)

    if username is None or len(username) == 0:
        return jsonify(dict(error='Username can not be empty')), 404

    user = db.session.query(models.User).filter_by(username=username).first()

    if not user:
        return jsonify(dict(error='Username ' + username + ' doesn\'t exists')), 404

    studies = [dict(id=item.id, uid=item.uid, accession_number=item.accession_number, body_part=item.body_part,
                    numFindings=len(item.findings), favorite=item.favorite, patient_name=item.patient_name,
                    patient_id=item.patient_id, comment=item.comment, status=item.status,
                    finalized_as=item.finalized_as, analyzed_by_aidoc=item.analyzed_by_aidoc,
                    series=[dict(uid=series.uid, plane=series.plane, numFindings=len(series.findings),
                                 finding_statuses=sorted([finding.status for finding in series.findings]),
                                 finding_labels=sorted([finding.label for finding in series.findings]))
                            for series in item.series])
               for item in user.worklist]
    return jsonify(studies)


def scan_metadata_to_json(scan):
    shape = scan.size
    slices = shape[0]
    window_defs = app.config['DEFAULT_WINDOW_DEFS']
    if scan.body_part in window_defs:
        window = window_defs[scan.body_part]
    else:
        logging.warning('Unknown body part "%s" - using default brain window', scan.body_part)
        window = [35, 80]

    # TODO: sent bits allocated to the client so it can calculated the scan size in bytes
    return dict(
        uid=scan.uid,
        accessionNumber=scan.metadata.get('AccessionNumber', scan.uid),
        patientName=scan.name,
        bodyPart=scan.body_part,
        plane=scan.plane,
        slope=scan.metadata.get('RescaleSlope', 1),
        intercept=scan.metadata.get('RescaleIntercept', 0),
        windowCenter=window[0],
        windowWidth=window[1],
        slices=slices,
        rows=shape[1],
        columns=shape[2],
        color=scan.is_color_image(),
        pixelSpacing=scan.metadata.get('PixelSpacing', None),
        sliceThickness=scan.metadata.get('SliceThickness', None),
        frameOfReferenceUID=scan.metadata.get('FrameOfReferenceUID', None),
        imageOrientation=scan.image_orientation,
        imagePositions=scan.image_positions
    )


@app.route('/api/study/<uid>')
@login_required
def get_study_metadata(uid):
    try:
        work_item = get_work_item(uid)
        study_metadata = {
            'uid': uid,
            'accessionNumber': work_item.accession_number,
            'patientName': work_item.patient_name,
            'patientLocation': work_item.get_patient_location(),
            'series': {}
        }

        for series in work_item.series:
            # TODO: IB - the study metadata should be taken from the work-item\series models, and not loaded
            # TODO: from the file every time
            scan = Scan.fromID(series.uid, app.config['CT_SCANS_DIR'], read_volume=False)
            if work_item.body_part is not None:
                scan.body_part = work_item.body_part
            study_metadata['series'][series.id] = scan_metadata_to_json(scan)

        # check if the study has a report
        report_loader = reports.ReportsLoader(app.config['REPORTS_DIR'])
        report = report_loader.load_report(work_item.accession_number)

        study_metadata['report'] = report

        return jsonify(study_metadata)
    except IOError:
        app.logger.warning('Cannot find scan with id %s', uid)
        abort(404)
    except NoResultFound:
        app.logger.warning('Work list with uid %s not found for user: %s', uid, current_user.username)
        abort(404)


@app.route('/api/scan/<uid>')
@login_required
def get_scan(uid):
    try:

        scan = Scan.fromID(uid, app.config['CT_SCANS_DIR'], read_volume=False)
        scan_data = scan_metadata_to_json(scan)
        return jsonify(scan_data)
    except IOError:
        app.logger.warning('Cannot find scan with id %s', uid)
        abort(404)


@app.route('/api/scan/<uid>/volume')
@login_required
def get_scan_volume(uid):
    try:
        accept_encoding = request.headers.get('Accept-Encoding', '')
        prefer_compressed_volume = 'gzip' in accept_encoding.lower()

        scan = Scan.fromID(uid, app.config['CT_SCANS_DIR'], prefer_compressed_volume=prefer_compressed_volume,
                           compressed_volumes_dir=app.config['COMPRESSED_VOLUMES_DIR'])

        if not scan.volume_compressed:
            if prefer_compressed_volume:
                # compress asynchronously the scan so that next time will be faster
                app.logger.info('No compressed scan was found for %s, compressing...', uid)
                scan_compressor.compress(uid)

            volume = scan.volume.tobytes()
        else:
            volume = scan.volume

        headers = Headers()
        headers['Content-Length'] = len(volume)

        if scan.volume_compressed:
            headers['Content-Encoding'] = 'gzip'
            headers['Vary'] = 'Accept-Encoding'

        rv = app.response_class(volume, mimetype='application/octet-stream', headers=headers)
        # TODO: Add etag support
        return rv
    except IOError:
        app.logger.warning('Cannot find scan with id %s', uid)
        abort(404)


def get_work_item(work_item_uid):
    return db.session.query(models.WorkItem).filter_by(user_id=current_user.id, uid=work_item_uid).one()


@app.route('/api/worklist/<work_item_uid>/findings')
@login_required
def get_findings(work_item_uid):
    try:
        work_item = get_work_item(work_item_uid)
        return jsonify([x.to_json_dict() for x in work_item.findings])
    except NoResultFound:
        app.logger.warning('Work item with uid %s not found for user: %s', work_item_uid, current_user.username)
        return jsonify([])


@app.route('/api/worklist/<work_item_uid>/findings', methods=['POST'])
@login_required
def add_finding(work_item_uid):
    try:
        finding_json = request.get_json()
        work_item = get_work_item(work_item_uid)

        finding = models.Finding(work_item.id, finding_json['series_id'], None, 'new',
                                 finding_json.get('label', 'hemorrhage'),
                                 finding_json['key_slice'], finding_json['visualization_type'],
                                 json.dumps(finding_json['locations']), finding_json['order'], None,
                                 finding_json.get('comment', None))
        db.session.add(finding)
        db.session.commit()

        metric_dict = work_item.to_json_dict()
        metric_dict['username'] = current_user.username
        metric_dict.update(finding.to_json_dict())

        app_insights_client.track_metric('new-finding', 1, properties=metric_dict)

        return jsonify(finding.to_json_dict())
    except NoResultFound:
        app.logger.warning('Work item with uid %s not found for user: %s', work_item_uid, current_user.username)
        abort(500)


@app.route('/api/worklist/<work_item_uid>/findings/<id>', methods=['PUT'])
@login_required
def update_finding(work_item_uid, id):
    try:
        finding_json = request.get_json()
        work_item = get_work_item(work_item_uid)

        if int(id) != finding_json['id']:
            abort(400)

        finding = db.session.query(models.Finding).get(finding_json['id'])

        if finding:
            finding.status = finding_json['status']
            finding.locations = json.dumps(finding_json['locations'])

            if 'comment' in finding_json:
                finding.comment = finding_json['comment']

            db.session.commit()

            metric_dict = finding.to_json_dict()
            metric_dict['username'] = current_user.username
            app_insights_client.track_metric('updated-finding', 1, properties=metric_dict)
            return jsonify(finding.to_json_dict())
        else:
            abort(404)
    except NoResultFound:
        app.logger.warning('Work item with uid %s not found for user: %s', work_item_uid, current_user.username)
        abort(500)


@app.route('/api/worklist/<work_item_uid>/findings', methods=['PUT'])
@login_required
def batch_update_findings(work_item_uid):
    try:
        changes_json = request.get_json()
        work_item = get_work_item(work_item_uid)
        merged_changes = merge_changes(changes_json)
        results = {}

        if work_item.status == 'pending' and len(merged_changes) > 0:
            work_item.status = 'draft'

        for change in merged_changes:
            finding_json = change['finding']

            if change['type'] == 'new':
                try:
                    # Try to find this finding in the database (maybe it was already added before
                    finding = db.session.query(models.Finding).filter_by(
                        work_item_id=work_item.id, series_id=finding_json['series_id'], status='new',
                        label=finding_json['label'], key_slice=finding_json['key_slice'],
                        locations=json.dumps(finding_json['locations'])
                    ).one()

                    # If we found it, nothing more to do
                except NoResultFound:
                    # Need to add the finding to the DB
                    finding = models.Finding(work_item.id, finding_json['series_id'], None, 'new',
                                             finding_json.get('label', 'hemorrhage'),
                                             finding_json['key_slice'], finding_json['visualization_type'],
                                             json.dumps(finding_json['locations']), finding_json['order'], None,
                                             finding_json.get('comment', None))
                    db.session.add(finding)

                    metric_dict = work_item.to_json_dict()
                    metric_dict['username'] = current_user.username
                    metric_dict.update(finding.to_json_dict())
                    app_insights_client.track_metric('new-finding', 1, properties=metric_dict)

                results[finding_json['clientId']] = finding
            elif change['type'] == 'update':
                if 'id' in finding_json:
                    finding = db.session.query(models.Finding).get(finding_json['id'])
                    results[finding_json['id']] = finding
                elif 'clientId' in finding_json and 'prevFinding' in change:
                    # New finding that was updated before the client received its id - find it by looking at its
                    # previous version
                    prev_finding = change['prevFinding']
                    try:
                        finding = db.session.query(models.Finding).filter_by(
                            work_item_id=work_item.id, series_id=finding_json['series_id'], status='new',
                            label=prev_finding['label'], key_slice=prev_finding['key_slice'],
                            locations=json.dumps(prev_finding['locations'])
                        ).one()

                        results[finding_json['clientId']] = finding
                    except NoResultFound:
                        app.logger.warning('Invalid update for new finding: %s', json.dumps(change))
                        finding = None
                else:
                    app.logger.warning('Invalid update for new finding: %s', json.dumps(change))
                    finding = None

                if finding is not None:
                    finding.status = finding_json['status']
                    finding.locations = json.dumps(finding_json['locations'])

                    if 'comment' in finding_json:
                        finding.comment = finding_json['comment']

                    metric_dict = work_item.to_json_dict()
                    metric_dict['username'] = current_user.username
                    metric_dict.update(finding.to_json_dict())
                    app_insights_client.track_metric('updated-finding', 1, properties=metric_dict)
            elif change['type'] == 'remove':
                if 'id' in finding_json:
                    models.Finding.query.filter_by(
                        id=finding_json['id'], work_item_id=work_item.id, status='new'
                    ).delete()
                elif 'clientId' in finding_json:
                    models.Finding.query.filter_by(
                        work_item_id=work_item.id, series_id=finding_json['series_id'], status='new',
                        label=finding_json['label'], key_slice=finding_json['key_slice'],
                        locations=json.dumps(finding_json['locations'])
                    ).delete()
                else:
                    app.logger.warning('Invalid removal of user finding: %s', json.dumps(change))
            else:
                app.logger.warning('Unknown change type: %s', change['type'])

        db.session.commit()

        # Prepare results for client (must be in the save order as the list we got
        result_list = []

        for change in changes_json:
            finding = change['finding']
            if 'id' in finding and finding['id'] in results:
                result_list.append(results[finding['id']].to_json_dict())
            elif 'clientId' in finding and finding['clientId'] in results:
                result_list.append(results[finding['clientId']].to_json_dict())
            else:
                result_list.append(None)

        return jsonify(result_list)
    except NoResultFound:
        app.logger.warning('Work item with uid %s not found for user: %s', work_item_uid, current_user.username)
        abort(500)


def merge_changes(changes):
    # Merge multiple changes to the same finding in order to avoid unnecessary db calls
    def get_change_id(change):
        if 'id' in change['finding']:
            return str(change['finding']['id'])
        else:
            return change['finding'].get('clientId', None)

    changes_ = sorted(changes, key=get_change_id)
    grouped_changes = groupby(changes_, get_change_id)
    results = []

    for _, change_iter in grouped_changes:
        change_list = list(change_iter)

        if len(change_list) == 1:
            results.append(change_list[0])
        else:
            last_change = change_list[len(change_list) - 1]

            if 'id' in last_change['finding']:
                # Keep only the last change for each id
                results.append(last_change)
            else:
                # Keep only the last change (the update), but mark it as new if this is a new finding added in this
                # batch
                if change_list[0]['type'] == 'new' and last_change['type'] != 'remove':
                    last_change['type'] = 'new'

                results.append(last_change)
    return results


@app.route('/api/support/operator')
def get_support_operator():
    support_phone_filename = os.path.join(os.path.expanduser('~'), 'viewer-data', 'support-phone.txt')
    if os.path.isfile(support_phone_filename):
        with open(support_phone_filename) as f:
            return jsonify({'phone': f.read().strip().strip(' \r\n')})

    abort(403)


@app.route('/api/support/send-email', methods=['POST'])
@login_required
def send_email_to_support():
    support_data = request.get_json()
    if not support_data or 'description' not in support_data:
        abort(400)

    mail_sender.send_support_email(current_user, support_data['description'], support_data.get('studyUid', None))
    return jsonify({'status': 'success'})


@app.route('/api/admin/stats')
@login_required
def get_admin_stats():
    if not current_user.is_admin:
        abort(403)

    return jsonify(calculate_stats())


@app.route('/toolbox')
def render_toolbox_template():
    return app.send_static_file('toolbox.html')


@app.route('/findings')
def render_findings_window_template():
    return app.send_static_file('findings.html')


@app.route('/admin/users/upload-data', methods=['POST'])
@login_required
def upload():
    if not current_user.is_admin:
        abort(403)

    app.logger.info("Starting to upload files.")

    upload_json = {}

    try:
        overwrite = request.form.get('overwrite', False) if 'overwrite' in request.form else False

        upload_json['scansUpload'] = userDataUploader.upload_files(request.files.getlist("scanFiles"),
                                                                   app.config['CT_SCANS_DIR'], True)

        app.logger.info("Uploaded scans")

        upload_json['dicomsUpload'] = userDataUploader.upload_files(request.files.getlist("dicomFiles"),
                                                                   app.config['CT_SCANS_DIR'], True)

        app.logger.info("Uploaded DICOMs")

        upload_json['findingsUpload'] = userDataUploader.upload_files(request.files.getlist("findingFiles"),
                                                                      app.config['FINDINGS_DIR'], True)

        app.logger.info("Uploaded findings")

        upload_json['worklistsUpload'] = userDataUploader.upload_files(request.files.getlist("worklistFiles"),
                                                                       app.config['WORKLISTS_DIR'], True)

        app.logger.info("Uploaded worklists")

        # load the updated user data into the database
        dbLoader.load_worklists(request.files.getlist("worklistFiles"), overwrite)

        app.logger.info("Loaded worklists to the db")

        userDataUploader.clean()
    except Exception as e:
        upload_json['error'] = str(e)
        app.logger.exception(str(e))
        userDataUploader.clean()

        return jsonify(upload_json), 500

    return jsonify(upload_json)


@auto.doc()
@app.route('/api/export/worklist/<username>', methods=['GET'])
@login_required
def download_worklist(username):
    '''Download user worklist'''
    check_permissions(username)

    worklist_file = os.path.join(dbLoader.worklist_dir, username)
    if worklist_file:
        return send_from_directory(app.config['WORKLISTS_DIR'],
                                   username)
    else:
        return jsonify(dict(error='Username ' + username + ' doesn\'t exists')), 404


def check_permissions(username):
    if username != current_user.username and not current_user.is_admin:
        abort(403)


@app.route('/docs')
def docs():
    return auto.html()


@app.route('/api/loaded-study', methods=['POST'])
@login_required
def study_loaded_event():
    json_data = request.get_json()

    metric_dict = dict()
    metric_dict['username'] = current_user.username
    metric_dict['study_uid'] = json_data['study_uid']
    metric_dict['load_time_millis'] = json_data['load_time']

    app_insights_client.track_metric('loaded-study', 1, properties=metric_dict)
    return '', 200


@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/<path:my_path>')
def get_arbitrary_path(my_path):
    return app.send_static_file('index.html')


def shutdown():
    mail_sender.destroy()
    scan_compressor.destroy()


atexit.register(shutdown)


def init_app_options():
    global app_options, arg_kv
    app_options = {}
    if 'pydevd' in sys.modules:  # running in pycharm
        app_options["debug"] = True
        app_options["use_debugger"] = True
        app_options["use_reloader"] = False
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            arg_kv = arg.split('=')
            if len(arg_kv) != 2:
                raise ValueError(f'Illegal named argument {arg_kv}')

            app_options[arg_kv[0]] = arg_kv[1]


if __name__ == "__main__":
    with app.app_context():
        dbLoader.load_data()
    init_app_options()

    app.logger.info('Starting server at port: 5000')
    app.run(**app_options)
