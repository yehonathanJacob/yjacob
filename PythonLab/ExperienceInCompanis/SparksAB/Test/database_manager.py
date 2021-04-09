import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

PATH_TO_DB = os.path.join(os.getcwd(), "pythonsqlite.db")

engine = create_engine("sqlite:///{}".format(PATH_TO_DB))

_Session = sessionmaker(bind=engine)
Base = declarative_base()
Base.metadata.reflect(engine)


@contextmanager
def AIDBSession():
    try:
        session = _Session()
        yield session
    except Exception as e:
        raise e
