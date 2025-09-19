from django.contrib import admin
from django.urls import path, include
from api.views import BookListAPIView as BookList

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),  # Maps to the BookList view
]