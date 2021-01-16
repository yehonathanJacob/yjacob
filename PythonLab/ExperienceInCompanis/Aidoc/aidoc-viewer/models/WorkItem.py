from config import DEFAULT_WINDOW_DEFS
from utils.db import db
from _datetime import datetime
from flask import current_app
from utils import common

from dicomaizer.common.uid import string2hash

patientLocations = ['Emergency', 'Inpatient', 'Outpatient']


class WorkItem(db.Model):
    __tablename__ = 'work_items'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    uid = db.Column(db.String)                 # Study Instance UID
    accession_number = db.Column(db.String, index=True)
    patient_name = db.Column(db.String)
    patient_id = db.Column(db.String)
    study_date = db.Column(db.String)
    study_time = db.Column(db.String)
    body_part = db.Column(db.String, db.Enum(*DEFAULT_WINDOW_DEFS.keys()))
    status = db.Column(db.String)
    finalized_as = db.Column(db.String, db.Enum('positive', 'negative'))
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    comment = db.Column(db.String)
    massive_bleeding = db.Column(db.Boolean, default=False)
    favorite = db.Column(db.Boolean, default=False)
    analyzed_by_aidoc = db.Column(db.Boolean, default=False)
    location = db.Column(db.String, db.Enum(*patientLocations))
    order_by = db.Column(db.Integer)

    series = db.relationship('Series', order_by='Series.created_on')
    findings = db.relationship('Finding', order_by='Finding.order')

    db.UniqueConstraint('user_id', 'uid', name='user_work_item_uq')

    def __init__(self, user_id, uid, accession_number, patient_name, patient_id, study_date, study_time, body_part, status='pending', analyzed_by_aidoc=True):
        self.user_id = user_id
        self.uid = uid
        self.accession_number = accession_number
        self.patient_name = patient_name
        self.patient_id = patient_id
        self.study_date = study_date
        self.study_time = study_time
        self.body_part = body_part
        self.status = status
        self.analyzed_by_aidoc = analyzed_by_aidoc

    def __repr__(self):
        return "<WorkItem(uid='%s', accession_number='%s', patient_name='%s', body_part='%s', status='%s')>" %\
               (self.uid, self.accession_number, self.patient_name, self.body_part, self.status)

    def get_patient_location(self):
        if self.location is not None:
            return self.location
        else:
            def generate_patient_location():
                if self.patient_name:
                    return patientLocations[int(string2hash(self.patient_name)) % len(patientLocations)]
                else:
                    return patientLocations[0]
            return generate_patient_location()

    def to_json_dict(self):
        dt = self.format_study_datetime()

        # calculate AI Findings column
        ai_findings = self.calc_ai_findings()
        return {
            'uid': self.uid,
            'accessionNumber': self.accession_number,
            'patientName': self.patient_name,
            'patientId': self.patient_id if self.patient_id else '-',
            'patientLocation': self.get_patient_location(),
            'studyTime':  dt,
            'bodyPart': self.body_part,
            'status': self.status,
            'massiveBleeding': self.massive_bleeding,
            'favorite': self.favorite,
            'finalized_as': self.finalized_as if self.finalized_as else '',
            'analyzed_by_aidoc': True if self.analyzed_by_aidoc is None else self.analyzed_by_aidoc,
            'ai_findings': ai_findings,
            'order_by': self.order_by
        }

    def calc_ai_findings(self):
        ai_findings_set = set()
        for f in self.findings:
            ai_findings_set.add(f.label)

        if len(ai_findings_set) < 3:
            return ', '.join(ai_findings_set)
        else:
            return 'Multi-Trauma'

    def format_study_datetime(self):
        if self.study_date and self.study_time:
            try:
                # handle milliseconds
                study_time = self.study_time[0:6]
                dt = datetime.strptime(self.study_date + study_time, '%Y%m%d%H%M%S')
                dt = dt.strftime(current_app.config.get('DATETIME_FORMAT'))
            except Exception:
                dt = '-'
        else:
            dt = '-'
        return dt
