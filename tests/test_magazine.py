import pytest
from lib.models.magazine import Magazine
from lib.models.author import Author
from lib.models.article import Article
from lib.db.connection import get_connection


@pytest.fixture(autouse=True)
def setup_db():
    # Reset the DB schema before each test
    with get_connection() as conn:
        with open("lib/db/schema.sql") as f:
            conn.executescript(f.read())


def test_magazine_save_and_find_by_id():
    mag = Magazine("Tech Today", "Technology")
    mag.save()
    assert mag.id is not None

    found = Magazine.find_by_id(mag.id)
    assert found is not None
    assert found.name == "Tech Today"
    assert found.category == "Technology"


def test_magazine_find_by_name():
    mag = Magazine("Health Weekly", "Health")
    mag.save()

    found = Magazine.find_by_name("Health Weekly")
    assert found is not None
    assert found.name == "Health Weekly"


def test_magazine_update_existing_record():
    mag = Magazine("Science Daily", "Science")
    mag.save()

    mag.name = "Science Monthly"
    mag.category = "Science & Tech"
    mag.save()

    updated = Magazine.find_by_id(mag.id)
    assert updated.name == "Science Monthly"
    assert updated.category == "Science & Tech"


def test_magazine_articles_and_article_titles():
    author = Author("Author One")
    author.save()

    mag = Magazine("Nature Mag", "Nature")
    mag.save()

    # Add articles to the magazine
    article1 = Article("Article One", author.id, mag.id)
    article1.save()
    article2 = Article("Article Two", author.id, mag.id)
    article2.save()

    articles = mag.articles()
    assert len(articles) == 2
    assert all(isinstance(a, Article) for a in articles)
    titles = mag.article_titles()
    assert "Article One" in titles
    assert "Article Two" in titles


def test_magazine_contributors_returns_authors():
    author1 = Author("Author A")
    author2 = Author("Author B")
    author1.save()
    author2.save()

    mag = Magazine("Contrib Mag", "Misc")
    mag.save()

    from lib.models.article import Article
    article1 = Article("Title 1", author1.id, mag.id)
    article2 = Article("Title 2", author2.id, mag.id)
    article1.save()
    article2.save()

    contributors = mag.contributors()
    assert len(contributors) == 2

    contributor_names = [author.name for author in contributors]
    assert "Author A" in contributor_names
    assert "Author B" in contributor_names
