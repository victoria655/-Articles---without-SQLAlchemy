from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

# Example usage for debugging
print("🧪 Debugging Session Started")

# Create and save a new author
author = Author(name="Jane Doe")
author.save()

# Create and save a new magazine
mag = Magazine(name="Tech Monthly", category="Technology")
mag.save()

# Create and save a new article
article = Article(title="AI in 2025", author_id=author.id, magazine_id=mag.id)
article.save()

# Fetch articles by author
print("📄 Articles by Jane Doe:")
for art in author.articles():
    print(art)

# Fetch magazines by author
print("📚 Magazines contributed to by Jane Doe:")
for m in author.magazines():
    print(m)
