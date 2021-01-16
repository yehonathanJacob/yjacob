import os
from models import models
from utils.db import db
import json
import zipfile


def set_all_edit_status(user, finding_status, work_item_status):
    work_items = db.session.query(models.WorkItem).filter_by(user_id=user.id).all()
    for wi in work_items:
        set_edit_status(wi, finding_status, work_item_status)


def set_edit_status(wi, finding_status, work_item_status):
    wi.status = work_item_status
    series = db.session.query(models.Series). \
        filter(models.Series.work_item_id == wi.id)
    for seria in series:
        findings = db.session.query(models.Finding). \
            filter(models.Finding.series_id == seria.id).order_by(models.Finding.order)

        for finding in findings:
            finding.status = finding_status
            finding.comment = None
    db.session.commit()


def set_type(wi, type):
    series = db.session.query(models.Series). \
        filter(models.Series.work_item_id == wi.id)
    for seria in series:
        findings = db.session.query(models.Finding). \
            filter(models.Finding.series_id == seria.id).order_by(models.Finding.order)

        for finding in findings:
            finding.visualization_type = type
    db.session.commit()


def delete_all_rejected_findings(user):
    deleted_count = 0
    work_items = db.session.query(models.WorkItem).filter_by(user_id=user.id).all()
    for wi in work_items:
        deleted = delete_rejected_findings(wi)
        if deleted:
            deleted_count += 1

    return deleted_count


def delete_all_user_findings(user):
    deleted_count = 0
    work_items = db.session.query(models.WorkItem).filter_by(user_id=user.id).all()
    for wi in work_items:
        deleted_count += delete_all_wi_findings(wi)
    return deleted_count


def delete_all_wi_findings(work_item):
    deleted_count = 0
    series = db.session.query(models.Series). \
        filter(models.Series.work_item_id == work_item.id)
    for seria in series:
        findings = db.session.query(models.Finding). \
            filter(models.Finding.series_id == seria.id).order_by(models.Finding.order)

        for finding in findings:
            db.session.delete(finding)
            deleted_count += 1
    work_item.status = 'pending'
    db.session.commit()
    return deleted_count


def delete_rejected_findings(work_item):
    deleted = False
    series = db.session.query(models.Series). \
        filter(models.Series.work_item_id == work_item.id)
    draft_count = 0
    for seria in series:
        findings = db.session.query(models.Finding). \
            filter(models.Finding.series_id == seria.id).order_by(models.Finding.order)

        for finding in findings:
            if finding.status == 'disapproved':
                db.session.delete(finding)
                deleted = True
            elif finding.status != 'pristine':
                draft_count += 1

    if draft_count == 0:
        work_item.status = 'pending'
    db.session.commit()
    return deleted


def export_findings(user, output_dir, should_extend=False):
    os.makedirs(output_dir, exist_ok=True)

    work_items = db.session.query(models.WorkItem).filter_by(user_id=user.id).all()

    # Create zip file
    zf = zipfile.ZipFile(user.username + "_findings.zip", "w")

    for wi in work_items:
        series = db.session.query(models.Series). \
            filter(models.Series.work_item_id == wi.id)

        for seria in series:
            counter = 1

            json_result = dict(type='hemorrhage')
            finding_dict = dict()
            series_uid = seria.uid

            findings = db.session.query(models.Finding). \
                filter(models.Finding.series_id == seria.id).order_by(models.Finding.order)

            # For each series_uid, we want to take all the findings, and put them in a findings dictionary
            # (a.k.a finding_dict).
            # Remove all the items with 'delete' in the comment.
            for finding in findings:
                add_finding = True
                if type(finding.comment) == str:
                    if 'delete' in finding.comment:
                        add_finding = False

                if add_finding:

                    data = dict(key_slice=finding.key_slice,
                                slice_dict=json.loads(finding.locations),
                                visualization_type=finding.visualization_type)
                    if should_extend:
                        data['status'] = finding.status
                        data['comment'] = finding.comment
                        data['input_source_index'] = finding.input_source_index
                        data['label'] = finding.label

                    finding_dict[str(counter)] = data
                    counter += 1

            json_result["finding_dict"] = finding_dict

            findings_file = os.path.join(output_dir, series_uid + '.json')
            with open(findings_file, 'w') as f:
                f.write(json.dumps(json_result, indent=4))

            zf.write(findings_file)

    zf.close()
    return zf.filename
