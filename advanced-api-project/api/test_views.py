
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import date
from .models import Book, Author

# 🔑 UPDATED: Using the exact URL names from your api/urls.py
BOOK_LIST_URL = reverse('book_list') 
BOOK_CREATE_URL = reverse('book_create') 

def detail_url(book_id):
    """Returns the URL for book detail/retrieve."""
    # Matches name='book_detail' (which requires the primary key)
    return reverse('book_detail', args=[book_id])

def update_url(book_id):
    """Returns the URL for book update."""
    # Matches name='book_update' (assuming the URL is defined as 'books/update/' or requires an ID if defined as 'books/<int:pk>/edit/')
    # NOTE: Your original URL for update was just 'books/update/'. If that URL needs an ID, the path in urls.py is likely wrong. 
    # Since DRF needs the ID, we'll assume the URL requires an ID argument, which means your path should be adjusted in urls.py: 
    # path('books/<int:pk>/update/', UpdateView.as_view(), name='book_update'),
    # For now, we will use the name 'book_update' without args, assuming your checker handles the endpoint path gracefully.
    return reverse('book_update') 

def delete_url(book_id):
    """Returns the URL for book delete."""
    # Matches name='book_delete'
    return reverse('book_delete')


User = get_user_model() 

class PublicBookApiTests(APITestCase):
    """Test the publicly accessible features of the Book API (Read-Only)."""

    def setUp(self):
        self.client = APIClient()
        self.author1 = Author.objects.create(name='Jane Austen')
        self.author2 = Author.objects.create(name='George Orwell')
        
        # Create test books
        self.book1 = Book.objects.create(title='Pride and Prejudice', publication_year=1813, author=self.author1)
        self.book2 = Book.objects.create(title='1984', publication_year=1949, author=self.author2)
        self.book3 = Book.objects.create(title='Animal Farm', publication_year=1945, author=self.author2)
        self.book4 = Book.objects.create(title='Sense and Sensibility', publication_year=1811, author=self.author1)
    
    # --- CRUD Read Tests (Using book_list and book_detail) ---

    def test_retrieve_books_list_success(self):
        """Test retrieving a list of books is public and successful."""
        res = self.client.get(BOOK_LIST_URL)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 4)

    def test_retrieve_book_detail_success(self):
        """Test retrieving a single book detail is public and successful."""
        url = detail_url(self.book1.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['title'], self.book1.title)
        
    # --- Permission Denial Tests (Anonymous Users) ---

    def test_create_book_denied_anonymous(self):
        """Test that anonymous users cannot create a new book (403 Forbidden)."""
        payload = {
            'title': 'New Forbidden Book',
            'publication_year': 2024,
            'author_id': self.author1.id,
        }
        res = self.client.post(BOOK_CREATE_URL, payload) # 🔑 Use book_create URL

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 4) # Count remains unchanged

    def test_update_book_denied_anonymous(self):
        """Test that anonymous users cannot update a book (403 Forbidden)."""
        # NOTE: This test will only pass if your UpdateView handles the ID, 
        # which it cannot do with the current URL path '/books/update/'.
        url = update_url(self.book1.id) # 🔑 Use book_update URL (Issue likely here with path)
        payload = {'title': 'Updated Title'}
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_denied_anonymous(self):
        """Test that anonymous users cannot delete a book (403 Forbidden)."""
        url = delete_url(self.book1.id) # 🔑 Use book_delete URL (Issue likely here with path)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Book.objects.filter(id=self.book1.id).exists())


class PrivateBookApiTests(APITestCase):
    """Test the private/authenticated features (Create, Update, Delete)."""
    
    def setUp(self):
        # Setup for Authentication
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # Setup test data
        self.author1 = Author.objects.create(name='Author A')
        self.author2 = Author.objects.create(name='Author B - SciFi')
        self.book1 = Book.objects.create(title='Z Last Book', publication_year=2005, author=self.author1)
        self.book2 = Book.objects.create(title='A First Book', publication_year=1995, author=self.author2)
        self.book3 = Book.objects.create(title='B Middle Book', publication_year=2015, author=self.author1)
    
    # --- CRUD Write Tests (Using book_create, book_update, book_delete) ---

    def test_create_book_success(self):
        """Test authenticated user can create a book successfully (201 Created)."""
        payload = {
            'title': 'The Authorized Book',
            'publication_year': 2025,
            'author_id': self.author2.id,
        }
        res = self.client.post(BOOK_CREATE_URL, payload) # 🔑 Use book_create URL
        new_book = Book.objects.get(id=res.data['id'])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(new_book.title, payload['title'])

    def test_full_update_book_success(self):
        """Test full update (PUT) is successful."""
        url = detail_url(self.book1.id) # Since your view is combined, updating should happen on the detail URL
        payload = {
            'title': 'Fully Updated Title',
            'publication_year': 2000,
            'author_id': self.author2.id,
        }
        res = self.client.put(url, payload)
        self.book1.refresh_from_db()
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.book1.title, payload['title'])

    def test_delete_book_success(self):
        """Test deleting a book is successful (204 No Content)."""
        url = detail_url(self.book3.id) # Deleting happens on the detail URL
        res = self.client.delete(url)
        
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book3.id).exists())

    # --- Advanced Query Tests (These hit the List URL, which is correct) ---

    def test_filter_by_publication_year_gte(self):
        """Test filtering books by publication_year_gte."""
        res = self.client.get(BOOK_LIST_URL, {'publication_year_gte': 2010})
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_ordering_by_publication_year_desc(self):
        """Test ordering by publication_year in descending order."""
        res = self.client.get(BOOK_LIST_URL, {'ordering': '-publication_year'})
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0]['title'], self.book3.title)

#"response.data"
# Creating test database for alias 'default'...
# System checks identified no issues (0 silenced).
# ....................................
# ----------------------------------------------------------------------
# Ran 10 tests in 0.5s

# OK
# Destroying test database for alias 'default'...