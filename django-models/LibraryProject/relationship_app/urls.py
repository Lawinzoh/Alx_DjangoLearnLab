from django import views
from django.urls import path
from .views import SignUpView, list_books, LibraryDetailView
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('books/', list_books, name='list_books'), # Function based view
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'), # Class based view
    path("register/", views.register, name="register"), # User registration
    path("login/", LoginView.as_view(template_name="registration/login.html"), name="login"), # User login
    path("logout/", LogoutView.as_view(template_name="registration/logout.html"), name="logout"), # User logout
    path("admin-view/", views.admin_view, name="admin_view"), # Admin only view
    path("librarian-view/", views.librarian_view, name="librarian_view"), # Librarian only view
    path("member-view/", views.member_view, name="member_view"), # Member only view
    path("add_book/", views.add_book, name="add_book"), # Add book view
    path("edit_book/<int:book_id>/", views.edit_book, name="edit_book"), # Edit book view
    path("delete_book/<int:book_id>/", views.delete_book, name="delete_book"), # Delete book view
]