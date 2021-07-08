import os
from contextlib import contextmanager
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

PATH_TO_DB = os.path.join(os.getcwd(), 'assiment2', "pythonsqlite.db")

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

class CrawlingResults(Base):
    __table__ = Base.metadata.tables['crawling_results']

    @classmethod
    def insert_df(cls, df: pd.DataFrame):
        with AIDBSession() as session:
            engine = session.get_bind()
            df.to_sql(cls.__table__.name, con=engine, if_exists='append', index=False)