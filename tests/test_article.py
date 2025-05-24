import pytest
from lib.models.article import Article
from lib.models.author import Author
from lib.models.magazine import Magazine

def test_article_save_and_find_by_id():
    author = Author("Test Author")
    magazine = Magazine("Test Magazine", "Test Category")
    author.save()
    magazine.save()

    article = Article("Test Article", author.id, magazine.id)
    article.save()

    found = Article.find_by_id(article.id)
    assert found is not None
    assert found.id == article.id
    assert found.title == "Test Article"
    assert found.author_id == author.id
    assert found.magazine_id == magazine.id

def test_article_update_existing_record():
    author = Author("Update Author")
    magazine = Magazine("Update Magazine", "Updates")
    author.save()
    magazine.save()

    article = Article("Original Title", author.id, magazine.id)
    article.save()

    article.title = "Updated Title"
    article.save()

    updated = Article.find_by_id(article.id)
    assert updated.title == "Updated Title"


def test_article_find_by_id_not_found_returns_none():
    assert Article.find_by_id(-1) is None

def test_article_validation_rejects_empty_title():
    with pytest.raises(ValueError):
        Article("", 1, 1).save()
