import pytest
from lib.models.magazine import Magazine

def test_top_publisher_no_articles(monkeypatch):
    class FakeCursor:
        def execute(self, sql):
            pass  # do nothing

        def fetchone(self):
            return None

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

    class FakeConnection:
        def cursor(self):
            return FakeCursor()

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

    def fake_get_connection():
        return FakeConnection()

    # Patch the get_connection used inside magazine.py, not the original module!
    monkeypatch.setattr('lib.models.magazine.get_connection', fake_get_connection)

    result = Magazine.top_publisher()
    assert result is None
