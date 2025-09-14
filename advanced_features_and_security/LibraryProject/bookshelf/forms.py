from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        # Include the fields you want users to fill
        fields = ['title', 'author', 'publication_year']
        # Optional: Add widgets or labels if needed
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter book title'}),
            'author': forms.TextInput(attrs={'placeholder': 'Enter author name'}),
            'publication_year': forms.NumberInput(attrs={'placeholder': 'Enter year'}),
        }
        labels = {
            'title': 'Book Title',
            'author': 'Author',
            'publication_year': 'Year Published',
        }