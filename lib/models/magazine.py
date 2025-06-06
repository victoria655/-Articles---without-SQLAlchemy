from lib.db.connection import get_connection

class Magazine:
    def __init__(self, name, category, id=None):
        self.id = id
        self.name = name
        self.category = category

    def __repr__(self):
        return f"<Magazine {self.id}: {self.name} ({self.category})>"

    def save(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            if self.id:
                cursor.execute(
                    "UPDATE magazines SET name = ?, category = ? WHERE id = ?",
                    (self.name, self.category, self.id)
                )
            else:
                cursor.execute(
                    "INSERT INTO magazines (name, category) VALUES (?, ?)",
                    (self.name, self.category)
                )
                self.id = cursor.lastrowid
            conn.commit()  # Ensure changes are saved

    @classmethod
    def find_by_id(cls, mag_id):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM magazines WHERE id = ?", (mag_id,))
            row = cursor.fetchone()
            if row:
                return cls(id=row['id'], name=row['name'], category=row['category'])
            return None

    @classmethod
    def find_by_name(cls, name):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM magazines WHERE name = ?", (name,))
            row = cursor.fetchone()
            if row:
                return cls(id=row['id'], name=row['name'], category=row['category'])
            return None

    def articles(self):
        from lib.models.article import Article
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (self.id,))
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

    def contributors(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT au.* FROM authors au
                JOIN articles ar ON au.id = ar.author_id
                WHERE ar.magazine_id = ?
            """, (self.id,))
            rows = cursor.fetchall()
            from lib.models.author import Author
            return [
                Author(
                    id=row['id'],
                    name=row['name']
                )
                for row in rows
            ]

    def article_titles(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT title FROM articles WHERE magazine_id = ?", (self.id,))
            return [row['title'] for row in cursor.fetchall()]

    @classmethod
    def top_publisher(cls):
        sql = """
            SELECT magazine_id, COUNT(*) as article_count
            FROM articles
            GROUP BY magazine_id
            ORDER BY article_count DESC
            LIMIT 1
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                return cls.find_by_id(result["magazine_id"])
            return None
    
    @classmethod
    def all(cls):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM magazines")
            rows = cursor.fetchall()
            return [
                cls(
                    id=row['id'],
                    name=row['name'],
                    category=row['category']
                )
                for row in rows
            ]
