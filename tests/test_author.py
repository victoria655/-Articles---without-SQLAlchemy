import pytest
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.connection import get_connection


@pytest.fixture(autouse=True)
def setup_db():
    """Reset the in-memory DB for each test"""
    with get_connection() as conn:
        with open("lib/db/schema.sql") as f:
            conn.executescript(f.read())


def test_author_save_and_find_by_id():
    author = Author("John Doe")
    author.save()
    assert author.id is not None

    found = Author.find_by_id(author.id)
    assert found.name == "John Doe"
    assert found.id == author.id


def test_author_find_by_name():
    author = Author("Jane Doe")
    author.save()

    found = Author.find_by_name("Jane Doe")
    assert found is not None
    assert found.name == "Jane Doe"


def test_author_add_article_and_articles_method():
    author = Author("Alice")
    magazine = Magazine("Science Weekly", "Science")
    author.save()
    magazine.save()

    author.add_article(magazine, "Quantum Physics Today")

    articles = author.articles()
    assert len(articles) == 1
    assert isinstance(articles[0], Article)
    assert articles[0].title == "Quantum Physics Today"


def test_author_magazines_method():
    author = Author("Bob")
    mag1 = Magazine("Tech Daily", "Tech")
    mag2 = Magazine("Health Monthly", "Health")
    author.save()
    mag1.save()
    mag2.save()

    author.add_article(mag1, "AI in 2025")
    author.add_article(mag2, "Nutrition Basics")

    mags = author.magazines()
    assert len(mags) == 2
    names = [m.name for m in mags]
    assert "Tech Daily" in names
    assert "Health Monthly" in names


def test_author_topic_areas_returns_unique_categories():
    author = Author("Carol")
    mag1 = Magazine("Eco Today", "Environment")
    mag2 = Magazine("Bio Weekly", "Biology")
    mag3 = Magazine("Another Bio", "Biology")  # duplicate category
    author.save()
    mag1.save()
    mag2.save()
    mag3.save()

    author.add_article(mag1, "Climate Change")
    author.add_article(mag2, "DNA Structure")
    author.add_article(mag3, "Cell Growth")

    topic_areas = {m.category for m in author.magazines()}
    assert "Environment" in topic_areas
    assert "Biology" in topic_areas
    assert len(topic_areas) == 2


def test_author_name_validation():
    with pytest.raises(ValueError):
        Author("").save()
