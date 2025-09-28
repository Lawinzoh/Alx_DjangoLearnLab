import django_filters
from .models import Book

class BookFilter(django_filters.FilterSet):
    # Filter by publication year (allowing exact match, greater than, less than)
    publication_year = django_filters.NumberFilter(
        field_name='publication_year', 
        lookup_expr='exact'
    )
    publication_year_gte = django_filters.NumberFilter(
        field_name='publication_year', 
        lookup_expr='gte', 
        label='Publication Year (Greater Than or Equal)'
    )
    publication_year_lte = django_filters.NumberFilter(
        field_name='publication_year', 
        lookup_expr='lte', 
        label='Publication Year (Less Than or Equal)'
    )

    class Meta:
        model = Book
        # Fields for exact matching:
        fields = {
            'title': ['exact', 'icontains'], # Allows exact title match and case-insensitive partial search
            'author': ['exact'],            # Filter by Author ID (author=1)
            'publication_year': ['exact'],  # Redundant but kept for clean Meta definition
        }