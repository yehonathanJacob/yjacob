import os
import sqlite3

import nltk


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Exception as e:
        print(e)


sql_create_word_table = """
CREATE TABLE IF NOT EXISTS word_count (
    word character varying(256) PRIMARY KEY,
    count integer NOT NULL
);
"""

if __name__ == '__main__':
    # setup nltk
    nltk.download('stopwords')
    nltk.download('wordnet')

    # setup DB
    database = os.path.join(os.getcwd(), "pythonsqlite.db")
    conn = create_connection(database)
    if conn is not None:
        create_table(conn, sql_create_word_table)
    else:
        print("Error! cannot create the database connection.")
