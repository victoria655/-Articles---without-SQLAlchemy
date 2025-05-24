
import sqlite3

def get_connection():
    conn = sqlite3.connect('your_db_file.db')
    conn.row_factory = sqlite3.Row
    return conn





# import pytest
# import sqlite3
# from lib.models.article import Article
# from lib.models.author import Author
# from lib.models.magazine import Magazine

# @pytest.fixture
# def db():
#     conn = sqlite3.connect(":memory:")
#     conn.row_factory = sqlite3.Row
#     with open("lib/db/schema.sql") as f:
#         conn.executescript(f.read())
#     yield conn
#     conn.close()

# def test_article_save_and_find_by_id(db):
#     author = Author("Test Author")
#     magazine = Magazine("Test Magazine", "Test Category")
#     author.save(db)
#     magazine.save(db)

#     article = Article("Test Article", author.id, magazine.id)
#     article.save(db)

#     found = Article.find_by_id(db, article.id)
#     assert found is not None
#     assert found.id == article.id
#     assert found.title == "Test Article"
#     assert found.author_id == author.id
#     assert found.magazine_id == magazine.id

# def test_article_update_existing_record(db):
#     author = Author("Update Author")
#     magazine = Magazine("Update Magazine", "Updates")
#     author.save(db)
#     magazine.save(db)

#     article = Article("Original Title", author.id, magazine.id)
#     article.save(db)

#     article.title = "Updated Title"
#     article.save(db)

#     updated = Article.find_by_id(db, article.id)
#     assert updated.title == "Updated Title"

# def test_article_find_by_id_not_found_returns_none(db):
#     assert Article.find_by_id(db, -1) is None

# def test_article_validation_rejects_empty_title(db):
#     with pytest.raises(ValueError):
#         Article("", 1, 1).save(db)

