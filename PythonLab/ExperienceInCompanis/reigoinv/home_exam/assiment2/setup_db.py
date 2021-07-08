import os
import sqlite3

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
    c = conn.cursor()
    c.execute(create_table_sql)


sql_create_word_table = """
CREATE TABLE IF NOT EXISTS crawling_results (
    id serial  primary key,
    number_of_bedrooms integer NOT NULL,
    number_of_bathrooms integer NOT NULL,
    property_size integer NOT NULL,
    sold_date character varying(256) NOT NULL,
    property_price integer NOT NULL,
    walk_score integer NOT NULL,
    transit_score integer NOT NULL,
    great_schools character varying(1024) NOT NULL
);
"""

if __name__ == '__main__':
    # setup DB
    database = os.path.join(os.getcwd(), "pythonsqlite.db")
    conn = create_connection(database)
    if conn is not None:
        create_table(conn, sql_create_word_table)
    else:
        print("Error! cannot create the database connection.")
