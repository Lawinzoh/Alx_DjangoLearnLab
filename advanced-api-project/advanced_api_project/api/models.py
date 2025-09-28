from django.db import models

# # The Author model represents a book author in the system.
# Each author can be linked to multiple books (one-to-many relationship).
class Author(models.Model):
    name = models.CharField(max_length=100)


# The Book model represents individual books in the system.
# Each book is linked to exactly one Author through a foreign key.
# ForeignKey establishes a one-to-many relationship (one Author -> many Books).
    # related_name="books" allows accessing all books by an author using author.books.
class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)