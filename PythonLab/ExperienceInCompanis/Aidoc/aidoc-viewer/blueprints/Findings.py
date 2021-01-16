from flask import Blueprint, request, abort, jsonify, send_file
from flask_login import current_user
from flask_login import login_required

from models import models
from utils.db import db
from utils.findings_util import set_all_edit_status, set_edit_status, delete_rejected_findings, \
    delete_all_rejected_findings, export_findings, set_type, delete_all_wi_findings, delete_all_user_findings
from utils.autodoc import auto

findings = Blueprint('findings', __name__)


# prefix /api/admin/findings

@auto.doc()
@findings.route('/pristinize/<username>')
@login_required
def pristinize_finding_status(username):
    '''IRREVERSIBLE - sets all the findings status to pristine'''
    if username != current_user.username and not current_user.is_admin:
        abort(403)

    try:
        user = db.session.query(models.User).filter_by(username=username).first()

        if len(request.args) > 0:
            study_uid = request.args.get('uid')
            work_item = models.WorkItem.query.filter_by(
                uid=study_uid, user_id=user.id).first()

            if work_item:
                set_edit_status(work_item, 'pristine', 'pending')
            else:
                return jsonify({'status': 'Fail', 'error': 'No study %s found in %s worklist' % (study_uid, username)})

        else:
            set_all_edit_status(user, 'pristine', 'pending')
        return jsonify({'status': 'Success'})
    except Exception as e:
        return jsonify({'status': 'Fail', 'error': str(e)})


@auto.doc()
@findings.route('/edit/<username>')
@login_required
def edit_findings(username):
    '''Changes findings status to allow editing'''
    if username != current_user.username and not current_user.is_admin:
        abort(403)

    try:
        user = db.session.query(models.User).filter_by(username=username).first()

        if len(request.args) > 0:
            study_uid = request.args.get('uid')
            work_item = models.WorkItem.query.filter_by(
                uid=study_uid, user_id=user.id).first()

            if work_item:
                set_edit_status(work_item, 'new', 'draft')
            else:
                return jsonify({'status': 'Fail', 'error': 'No study %s found in %s worklist' % (study_uid, username)})

        else:
            set_all_edit_status(user, 'new', 'draft')
        return jsonify({'status': 'Success'})
    except Exception as e:
        return jsonify({'status': 'Fail', 'error': str(e)})


@auto.doc()
@findings.route('/set-type/<username>/<type>')
@login_required
def set_findings_type(username, type):
    '''IRREVERSIBLE - Set findings type to given type - arrow, box'''
    if username != current_user.username and not current_user.is_admin:
        abort(403)

    try:
        user = db.session.query(models.User).filter_by(username=username).first()

        if len(request.args) > 0:
            study_uid = request.args.get('uid')
            work_item = models.WorkItem.query.filter_by(
                uid=study_uid, user_id=user.id).first()

            if work_item:
                set_type(work_item, type)
            else:
                return jsonify({'status': 'Fail', 'error': 'No study %s found in %s worklist' % (study_uid, username)})

        else:
            work_items = db.session.query(models.WorkItem).filter_by(user_id=user.id).all()
            for wi in work_items:
                set_type(wi, type)
        return jsonify({'status': 'Success', 'updated': len(work_items)})
    except Exception as e:
        return jsonify({'status': 'Fail', 'error': str(e)})



@auto.doc()
@findings.route('/rejected/<username>')
@login_required
def delete_disapproved_findings(username):
    '''IRREVERSIBLE'''
    if username != current_user.username and not current_user.is_admin:
        abort(403)

    try:
        user = db.session.query(models.User).filter_by(username=username).first()

        if len(request.args) > 0:
            study_uid = request.args.get('study_uid')
            work_item = models.WorkItem.query.filter_by(
                uid=study_uid, user_id=user.id).first()

            if work_item:
                deleted = delete_rejected_findings(work_item)
                if deleted:
                    return jsonify({'status': 'Success'})
                else:
                    return jsonify({'status': 'Fail', 'error': 'Only rejected studies can be deleted'})
            else:
                return jsonify({'status': 'Fail', 'error': 'No study %s found in %s worklist' % (study_uid, username)})

        else:
            deleted = delete_all_rejected_findings(user)
            return jsonify({'status': 'Success', 'deleted': deleted})
    except Exception as e:
        return jsonify({'status': 'Fail', 'error': str(e)})


@auto.doc()
@findings.route('/delete-all-findings/<username>')
@login_required
def delete_all_findings(username):
    '''IRREVERSIBLE - Delete all findings for given user'''
    if username != current_user.username and not current_user.is_admin:
        abort(403)

    try:
        user = db.session.query(models.User).filter_by(username=username).first()
        if len(request.args) > 0:
            study_uid = request.args.get('study_uid')
            work_item = models.WorkItem.query.filter_by(
                uid=study_uid, user_id=user.id).first()

            if work_item:
                deleted_count = delete_all_wi_findings(work_item)
                try:
                    return jsonify({'status': 'Success', 'deleted_count': deleted_count})
                except:
                    return jsonify({'status': 'Failed for unknown reason'})
            else:
                return jsonify({'status': 'Fail', 'error': 'No study %s found in %s worklist' % (study_uid, username)})
        else:
            deleted_count = delete_all_user_findings(user)

            return jsonify({'status': 'Success', 'deleted_count': deleted_count})
    except Exception as e:
        return jsonify({'status': 'Fail', 'error': str(e)})


@auto.doc()
@findings.route('/download-findings/<username>', methods=['GET'])
@login_required
def download_findings(username):
    '''Export user findings'''
    if username != current_user.username and not current_user.is_admin:
        abort(403)

    if username is None or len(username) == 0:
        return jsonify(dict(error='Username can not be empty')), 404

    user = db.session.query(models.User).filter_by(username=username).first()

    if not user:
        return jsonify(dict(error='Username ' + username + ' doesn\'t exists')), 404

    findings_file = export_findings(user, "findings_export")

    return send_file(findings_file)


@auto.doc()
@findings.route('/download-findings-extended/<username>', methods=['GET'])
@login_required
def download_findings_extended(username):
    '''Export user findings with additional information'''
    if username != current_user.username and not current_user.is_admin:
        abort(403)

    if username is None or len(username) == 0:
        return jsonify(dict(error='Username can not be empty')), 404

    user = db.session.query(models.User).filter_by(username=username).first()

    if not user:
        return jsonify(dict(error='Username ' + username + ' doesn\'t exists')), 404

    findings_file = export_findings(user, "findings_export", True)

    return send_file(findings_file)
