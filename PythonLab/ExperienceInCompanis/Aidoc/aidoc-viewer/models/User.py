from flask_login import UserMixin
from sqlalchemy import Boolean
from sqlalchemy.orm import validates

from utils.db import db
from utils.Password import Password


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    name = db.Column(db.String(80))
    password = db.Column(Password)
    role = db.Column(db.String(20), server_default='user', nullable=False)
    email = db.Column(db.String(120))
    load_finding_files = db.Column(Boolean, server_default='1', nullable=False)

    created_on = db.Column(db.DateTime)
    last_login_on = db.Column(db.DateTime)
    last_login_from = db.Column(db.String(80))

    worklist = db.relationship('WorkItem', order_by='WorkItem.id')

    def __init__(self, username, name, password, created_on, email, role='user', load_finding_files=True):
        self.username = username
        self.name = name
        self.password = password
        self.role = role
        self.email = email
        self.created_on = created_on
        self.load_finding_files = load_finding_files

    def __repr__(self):
        return "<User(username='%s', name='%s')>" % (self.username, self.name)

    @validates('password')
    def _validate_password(self, key, password):
        return getattr(type(self), key).type.validator(password)

    @property
    def is_admin(self):
        return self.role == 'admin'

    def to_json_dict(self):
        last_login = "Never" if self.last_login_on is None else self.last_login_on.strftime('%Y-%m-%d')
        created_on = "Not Available" if self.created_on is None else self.created_on.strftime('%Y-%m-%d')
        last_login_from = "Not Available" if self.last_login_from is None else self.last_login_from
        email = "" if self.email is None else self.email
        load_finding_files = self.load_finding_files

        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'role': self.role,
            'created_on': created_on,
            'last_login_on': last_login,
            'email': email,
            'last_login_from': last_login_from,
            'load_finding_files': load_finding_files
        }
