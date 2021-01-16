import numpy as np
from sqlalchemy import and_
from sqlalchemy import or_
from sqlalchemy.sql import func, case

from utils.db import db
from models import models


def calculate_stats():
    work_items_subquery = db.session.query(
        models.WorkItem.id.label('work_item_id'),
        models.WorkItem.uid.label('work_item_uid'),
        models.WorkItem.user_id.label('user_id'),
        (func.count(models.Finding.id).label('detections')),
        (func.sum(
            case(
                [
                    (models.Finding.status == 'approved', 1)
                ],
                else_=0
            )
        ).label('approved')),
        (func.sum(
            case(
                [
                    (models.Finding.status == 'disapproved', 1)
                ],
                else_=0
            )
        ).label('disapproved')),
        (func.sum(
            case(
                [
                    (models.Finding.status == 'new', 1)
                ],
                else_=0
            )
        ).label('new'))
    ).outerjoin(models.Finding, models.WorkItem.id == models.Finding.work_item_id)\
        .filter(models.WorkItem.status == 'finalized')\
        .group_by(models.WorkItem.id, models.WorkItem.user_id)\
        .subquery()

    query = db.session.query(
        models.User.username,
        (func.count(work_items_subquery.c.work_item_id).label('total')),
        (func.sum(
            case(
                [
                    (or_(
                        work_items_subquery.c.approved > 0,
                        work_items_subquery.c.new > 0
                    ), 1)
                ],
                else_=0
            )
        ).label('real_positive')),
        (func.sum(
            case(
                [
                    (or_(
                        work_items_subquery.c.detections == 0,
                        and_(
                            work_items_subquery.c.detections > 0,
                            work_items_subquery.c.detections == work_items_subquery.c.disapproved
                        )
                    ), 1)
                ],
                else_=0
            )
        ).label('real_negative')),
        (func.sum(
            case(
                [
                    (work_items_subquery.c.approved > 0, 1)
                ],
                else_=0
            )
        ).label('true_positive')),
        (func.sum(
            case(
                [
                    (and_(
                        work_items_subquery.c.detections > 0,
                        work_items_subquery.c.detections == work_items_subquery.c.disapproved
                    ), 1)
                ],
                else_=0
            )
        ).label('false_positive')),
        (func.sum(
            case(
                [
                    (work_items_subquery.c.detections == 0, 1)
                ],
                else_=0
            )
        ).label('true_negative')),
        (func.sum(
            case(
                [
                    (and_(
                        work_items_subquery.c.detections > 0,
                        work_items_subquery.c.detections == work_items_subquery.c.new
                    ), 1)
                ],
                else_=0
            )
        ).label('false_negative')),
        (func.sum(work_items_subquery.c.approved).label('true_positive_findings')),
        (func.sum(work_items_subquery.c.disapproved).label('false_positive_findings'))
    ).join(work_items_subquery, models.User.id == work_items_subquery.c.user_id)\
        .filter(models.User.role == 'user')\
        .group_by(models.User.username)

    user_stats = query.all()

    results = {
        'scan': {},
        'findings': {},
        'totals': {}
    }

    eps = 1e-16     # Tiny number used to prevent division by zero

    for stat in user_stats:
        username, total, real_positive, real_negative, true_positive, false_positive, true_negative, false_negative,\
            true_positive_findings, false_positive_findings = stat

        results['scan'][username] = {
            'total': total,
            'realPositive': real_positive,
            'realNegative': real_negative,
            'truePositive': true_positive,
            'falsePositive': false_positive,
            'trueNegative': true_negative,
            'falseNegative': false_negative,
            'sensitivity': true_positive / (real_positive + eps),
            'specificity': true_negative / (real_negative + eps),
            'accuracy': (true_positive + true_negative) / (total + eps)
        }

        results['findings'][username] = {
            'total': true_positive_findings + false_positive_findings,
            'truePositive': true_positive_findings,
            'falsePositive': false_positive_findings,
            'precision': true_positive_findings / (true_positive_findings + false_positive_findings + eps)
        }

    grand_totals = np.sum([s[1:] for s in user_stats], axis=0)
    total, real_positive, real_negative, true_positive, false_positive, true_negative, false_negative,\
        true_positive_findings, false_positive_findings = grand_totals

    results['totals']['scan'] = {
        'total': total,
        'realPositive': real_positive,
        'realNegative': real_negative,
        'truePositive': true_positive,
        'falsePositive': false_positive,
        'trueNegative': true_negative,
        'falseNegative': false_negative,
        'sensitivity': true_positive / (real_positive + eps),
        'specificity': true_negative / (real_negative + eps),
        'accuracy': (true_positive + true_negative) / (total + eps)
    }

    results['totals']['findings'] = {
        'total': true_positive_findings + false_positive_findings,
        'truePositive': true_positive_findings,
        'falsePositive': false_positive_findings,
        'precision': true_positive_findings / (true_positive_findings + false_positive_findings + eps)
    }

    # Find accidental true positive scans (scans that with findings in wrong locations, that were still marked as
    # positive by the user)
    accidental_tp_query = db.session.query(
        models.User.username,
        work_items_subquery.c.work_item_uid
    ).join(work_items_subquery, models.User.id == work_items_subquery.c.user_id) \
        .filter(models.User.role == 'user') \
        .filter(work_items_subquery.c.approved == 0) \
        .filter(work_items_subquery.c.disapproved > 0) \
        .filter(work_items_subquery.c.new > 0)

    results['accidentalTruePositives'] = accidental_tp_query.all()

    return results
