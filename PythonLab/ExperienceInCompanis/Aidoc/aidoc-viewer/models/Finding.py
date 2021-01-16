import json
from sqlalchemy import Integer
from utils.db import db


class Finding(db.Model):
    __tablename__ = 'findings'

    id = db.Column(db.Integer, primary_key=True)
    work_item_id = db.Column(db.Integer, db.ForeignKey('work_items.id'))
    series_id = db.Column(db.Integer, db.ForeignKey('series.id'))
    finding_uid = db.Column(db.Integer)
    status = db.Column(db.String)
    label = db.Column(db.String(50))
    key_slice = db.Column(db.Integer)
    visualization_type = db.Column(db.String)
    locations = db.Column(db.String)
    original_locations = db.Column(db.String)
    order = db.Column(db.Integer)
    comment = db.Column(db.String)
    input_source_index = db.Column(Integer, server_default='0', nullable=False)
    contour = db.Column(db.String, server_default=None)

    def __init__(self, work_item_id, series_id, finding_uid, status, label, key_slice, visualization_type, locations, order,
                 original_locations=None, comment=None, input_source_index=0, contour = None):
        self.work_item_id = work_item_id
        self.series_id = series_id
        self.finding_uid = finding_uid
        self.status = status
        self.label = label
        self.key_slice = key_slice
        self.visualization_type = visualization_type
        self.locations = locations
        self.order = order
        self.original_locations = original_locations
        self.comment = comment
        self.input_source_index = input_source_index
        self.contour = contour

    def __repr__(self):
        return "<Finding(finding_uid='{}', status='{}', key_slice='{}')>".format(self.finding_uid, self.status,
                                                                                 self.key_slice)

    def to_json_dict(self):
        return {
            'id': self.id,
            'series_id': self.series_id,
            'finding_uid': self.finding_uid,
            'label': self.label,
            'status': self.status,
            'key_slice': self.key_slice,
            'visualization_type': self.visualization_type,
            'locations': json.loads(self.locations),
            'original_locations': None if self.original_locations is None else json.loads(self.original_locations),
            'comment': self.comment,
            'order': self.order,
            'input_source_index': self.input_source_index,
            'contour': None if self.contour is None else json.loads(self.contour)
        }
