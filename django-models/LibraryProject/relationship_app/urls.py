from django.urls import path
from relationship_app.views import book_list, LibraryDetailView

urlpatterns = [
    path('books/', book_list, name='book_list'), # Function based view
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'), # Class based view
]