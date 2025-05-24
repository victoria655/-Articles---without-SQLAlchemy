import sqlite3
def setup_db():
    conn=sqlite3.connect('articles.db')
    with open('lib/db/schema.sql','r') as f:
        sql=f.read()
    conn.executescript(sql)
    conn.commit()
    conn.close()
    print("Database schema created")

if __name__=="__main__":
    setup_db()