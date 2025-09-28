# library/views.py (or wherever your views file is)
from warnings import filters
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Book
from django.urls import reverse_lazy
from rest_framework import generics, filters
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .filters import BookFilter

# 1. ListView: Retrieves all books (R - Read All)
class ListView(ListView):
    model = Book
    template_name = 'library/book_list.html'
    context_object_name = 'books'

# 2. DetailView: Retrieves a single book by ID (R - Read One)
class DetailView(DetailView):
    model = Book
    template_name = 'library/book_detail.html'

# 3. CreateView: Adds a new book (C - Create)
class CreateView(CreateView):
    model = Book
    # Fields must match your Book model fields
    fields = ['title', 'publication_year', 'author']
    template_name = 'library/book_form.html'
    
    # After successful creation, it redirects to the book's detail page 
    # (requires get_absolute_url on the Book model, see below).

# 4. UpdateView: Modifies an existing book (U - Update)
class UpdateView(UpdateView):
    model = Book
    fields = ['title', 'publication_year', 'author']
    template_name = 'library/book_form.html'

# 5. DeleteView: Removes a book (D - Delete)
class DeleteView(DeleteView):
    model = Book
    template_name = 'library/book_confirm_delete.html'
    # Redirect to the book list after successful deletion
    success_url = reverse_lazy('book_list')

# --- R (List) and C (Create) View ---
class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    # 🔑 Permission Setup: 
    # - GET (List) is allowed for everyone.
    # - POST (Create) is restricted to authenticated users.
    permission_classes = [IsAuthenticatedOrReadOnly] 

    # 🔑 Custom Filter & Search, and Ordering Setup:
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        ]
    search_fields = ['^title', 'author__name']
    filterset_class = BookFilter # Reference the custom filter class
    ordering_fields = ['title', 'publication_year', 'author__name']
    ordering = ['title'] # Default ordering


    def perform_create(self, serializer):
        """
        Executes custom logic before saving a new Book instance.
        """
        print(f"LOG: Creating new book: {serializer.validated_data.get('title')}")
        serializer.save()

# --- R (Detail), U (Update), and D (Delete) View ---
class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    # 🔑 Permission Setup: 
    # - GET (Detail) is allowed for everyone.
    # - PUT/PATCH (Update) and DELETE are restricted to authenticated users.
    permission_classes = [IsAuthenticatedOrReadOnly]