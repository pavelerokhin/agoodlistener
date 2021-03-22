import sqlite3
from modules.persistence.errors import SQLiteConnectionError, QueryExecutionError


def create_db_if_needed_and_get_connection(db_file):
    """
    create connection to SQLite database
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        raise SQLiteConnectionError("error while connecting to db", e)

    return conn


def execute_query(conn, query, *, execute_script=True, is_to_commit=True):
    try:
        c = conn.cursor()
        if execute_script:
            result = c.executescript(query)
        else:
            result = c.execute(query)
        if is_to_commit:
            conn.commit()
        return result
    except sqlite3.Error as e:
        raise QueryExecutionError("error while executing query", e)
