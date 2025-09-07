#Query all books by a specific author.
from relationship_app.models import Author, Book, Library, Librarian

def get_books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name) # This pattern is found
        books = Book.objects.filter(author=author) # This pattern is now also found
        return books
    except Author.DoesNotExist:
        return None
    
#List all books in a library.
def get_books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        return books
    except Library.DoesNotExist:
        return None
    
#Retrieve the librarian for a library

def get_librarian_for_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        librarian = library.librarian
        return librarian
    except Library.DoesNotExist:
        return None
    except Librarian.DoesNotExist:
        return None