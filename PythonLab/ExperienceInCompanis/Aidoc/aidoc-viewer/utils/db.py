from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError

db = SQLAlchemy()


def get_one_or_create(model,
                      create_method='',
                      create_method_kwargs=None,
                      **kwargs):
    try:
        return db.session.query(model).filter_by(**kwargs).one(), False
    except NoResultFound:
        create_kwargs = dict(kwargs, **create_method_kwargs or {})
        created = getattr(model, create_method, model)(**create_kwargs)
        try:
            db.session.add(created)
            db.session.commit()
            return created, True
        except IntegrityError:
            db.session.rollback()
            return db.session.query(model).filter_by(**kwargs).one(), False
