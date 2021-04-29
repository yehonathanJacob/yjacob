import logging

from contextlib import contextmanager
from sqlalchemy import create_engine, MetaData, Table, Column
from sqlalchemy.orm import sessionmaker

REDSHIFT = 'redshift+psycopg2://user:password@host:port/db_name'
POSTGRES = 'postgres://user:password@host:port/db_name'

CONNECTION = POSTGRES

_engine = create_engine(CONNECTION, pool_pre_ping=True)
Session = sessionmaker(bind=_engine)
db = Session()

def execute_query(sql_query):
    with _engine.connect() as connection:
        result = connection.execute(sql_query)
    return result

@contextmanager
def AIDBSession():
    try:
        session = Session()
        yield session
    except Exception as e:
        logging.error('AI DB session raised an exception: {exception}'.format(exception=e))
        session.rollback()
        raise e
    finally:
        session.close()
