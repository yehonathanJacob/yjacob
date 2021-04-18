import pandas as pd

from database_manager import Base, AIDBSession

WORD_COUNT_TABLE_NAME = "word_count"


class WordCountColumnNames:
    word = "Word"
    count = "Count"


class WordCount(Base):
    __table__ = Base.metadata.tables[WORD_COUNT_TABLE_NAME]

    @classmethod
    def insert_df(cls, df: pd.DataFrame):
        with AIDBSession() as session:
            engine = session.get_bind()
            df.to_sql(cls.__table__.name, con=engine, if_exists='append', index=False)
