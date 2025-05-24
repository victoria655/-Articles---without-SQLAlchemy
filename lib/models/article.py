from lib.db.connection import get_connection

class Article:
    def __init__(self, title, author_id, magazine_id, id=None):
        self.id = id
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id
    

    def __repr__(self):
        return f"<Article {self.id}: {self.title}>"

    def save(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            if self.id:
                cursor.execute("UPDATE articles SET title = ?, author_id = ?, magazine_id = ? WHERE id = ?", (self.title, self.author_id, self.magazine_id, self.id))
            else:
                cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", (self.title, self.author_id, self.magazine_id))
                self.id = cursor.lastrowid

    @classmethod
    def find_by_id(cls, article_id):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM articles WHERE id = ?", (article_id,))
            row = cursor.fetchone()
            if row:
                return cls(id=row['id'], title=row['title'], author_id=row['author_id'], magazine_id=row['magazine_id'])
            return None
