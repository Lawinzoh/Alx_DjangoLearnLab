from django import forms
from .models import Book

# ------------------------------
# ModelForm for Book
# ------------------------------
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
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

# ------------------------------
# Example Form (Generic)
# ------------------------------
class ExampleForm(forms.Form):
    name = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={'placeholder': 'Enter your name'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Enter your message'})
    )
