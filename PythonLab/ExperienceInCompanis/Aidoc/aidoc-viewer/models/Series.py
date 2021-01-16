from utils.db import db


class Series(db.Model):
    __tablename__ = 'series'

    id = db.Column(db.Integer, primary_key=True)
    work_item_id = db.Column(db.Integer, db.ForeignKey('work_items.id'))
    uid = db.Column(db.String, index=True)                 # Series Instance UID
    plane = db.Column(db.String, db.Enum('axial', 'sagittal', 'coronal'))
    created_on = db.Column(db.DateTime, server_default=db.func.now(), index=True)
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    massive_bleeding = db.Column(db.Boolean, default=False)
    findings = db.relationship('Finding', order_by='Finding.order')

    def __repr__(self):
        return "<Series(uid='{}', plane='{}', massive_bleeding={})>".format(self.uid, self.plane, self.massive_bleeding)

    def to_json_dict(self):
        return {
            'uid': self.uid,
            'plane': self.plane,
            'massiveBleeding': self.massive_bleeding
        }
