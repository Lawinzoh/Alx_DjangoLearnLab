from django.urls import path
from .views import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    # Assuming these generic views are defined in your api/views.py
)

urlpatterns = [
    # 1. Retrieve All Books (ListView) - R (Read All)
    # Endpoint: /books/
    path('books/', ListView.as_view(), name='book_list'),
    
    # 2. Add New Book (CreateView) - C (Create)
    # Endpoint: /books/new/
    path('books/new/', CreateView.as_view(), name='book_create'),

    # 3. Retrieve Single Book (DetailView) - R (Read One)
    # Endpoint: /books/<id>/
    # The <int:pk> captures the primary key (ID) as an integer.
    path('books/<int:pk>/', DetailView.as_view(), name='book_detail'),

    # 4. Modify Existing Book (UpdateView) - U (Update)
    # Endpoint: /books/<id>/edit/
    path('books/<int:pk>/edit/', UpdateView.as_view(), name='book_update'),

    # 5. Remove a Book (DeleteView) - D (Delete)
    # Endpoint: /books/<id>/delete/
    path('books/<int:pk>/delete/', DeleteView.as_view(), name='book_delete'),
]