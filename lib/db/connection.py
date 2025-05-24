import sqlite3
from contextlib import contextmanager

DB_PATH ='articles.db'

@contextmanager
def get_connection():
    conn=sqlite3.connect(DB_PATH)
    conn.row_factory=sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise 
    finally:
        conn.close()
        