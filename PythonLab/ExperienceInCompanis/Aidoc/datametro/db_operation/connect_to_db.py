#TODO:
# 1. To create connecto_to_db + modesl
# 2. To inser using Python+pandas the data downloaded form Redash
# 3. To copy and run all the SQL metrics from Redash + self created in VRT metrics
import logging

from contextlib import contextmanager
from sqlalchemy import create_engine, MetaData, Table, Column
from sqlalchemy.orm import sessionmaker

import config

CONNECTION_TO_POSTGRESS = 'postgres://{user}:{password}@{host}/{db_name}'

CONNECTION = CONNECTION_TO_POSTGRESS.format(user=config.USER_NAME, password=config.PASSWORD,
                                                    host=config.HOST, db_name=config.DB_NAME)


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

