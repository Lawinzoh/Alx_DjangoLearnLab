from django.contrib import admin
from django.db import router
from django.urls import path, include
from api.views import BookListAPIView as BookList, BookViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')

urlpatterns = [
    # Route for the BookList view (ListAPIView)
    path('books/', BookList.as_view(), name='book-list'),
    path('', include(router.urls)),                       # Include the router URLs for BookViewSet (all CRUD operations)
    path('api/token/', obtain_auth_token, name='api_token_auth'),
]