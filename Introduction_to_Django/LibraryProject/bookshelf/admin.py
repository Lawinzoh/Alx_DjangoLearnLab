from django.contrib import admin
from .models import Book

# Register your models here.

class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publication_year")  # columns shown in the list view
    list_filter = ("publication_year", "author")  # filters on the right-hand side
    search_fields = ("title", "author")  # search box for quick lookups


# Register the model with the custom admin
admin.site.register(Book, BookAdmin)