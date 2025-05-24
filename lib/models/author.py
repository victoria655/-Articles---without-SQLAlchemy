from lib.db.connection import get_connection
from lib.models.magazine import Magazine


class Author:
    def __init__(self, name, id=None):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"<Author {self.id}: {self.name}>"

    def save(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            if self.id:
                cursor.execute(
                    "UPDATE authors SET name = ? WHERE id = ?",
                    (self.name, self.id)
                )
            else:
                cursor.execute(
                    "INSERT INTO authors (name) VALUES (?)",
                    (self.name,)
                )
                self.id = cursor.lastrowid

    @classmethod
    def find_by_id(cls, author_id):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM authors WHERE id = ?",
                (author_id,)
            )
            row = cursor.fetchone()
            if row:
                return cls(id=row['id'], name=row['name'])
            return None

    @classmethod
    def find_by_name(cls, name):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM authors WHERE name = ?",
                (name,)
            )
            row = cursor.fetchone()
            if row:
                return cls(id=row['id'], name=row['name'])
            return None

    def articles(self):
        from lib.models.article import Article
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM articles WHERE author_id = ?",
                (self.id,)
            )
            rows = cursor.fetchall()
            return [
                Article(
                    id=row['id'],
                    title=row['title'],
                    author_id=row['author_id'],
                    magazine_id=row['magazine_id']
                )
                for row in rows
            ]

    def magazines(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT m.* FROM magazines m
                JOIN articles a ON m.id = a.magazine_id
                WHERE a.author_id = ?
            """, (self.id,))
            rows = cursor.fetchall()
            return [
                Magazine(
                    id=row['id'],
                    name=row['name'],
                    category=row['category']
                )
                for row in rows
            ]

    def add_article(self, magazine, title):
        from lib.models.article import Article
        article = Article(
            title=title,
            author_id=self.id,
            magazine_id=magazine.id
        )
        article.save()
        return article
