from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Book
from .forms import ExampleForm, BookForm

# ------------------------------
# Create Book
# ------------------------------
@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)  # Form validates and sanitizes input
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'bookshelf/book_form.html', {'form': form})


# ------------------------------
# Edit Book
# ------------------------------
@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)  # Safely fetch instance
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'bookshelf/book_form.html', {'form': form})


# ------------------------------
# Delete Book
# ------------------------------
@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)  # Safely fetch instance
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})


# ------------------------------
# Book List & Search
# ------------------------------
@login_required
def book_list(request):
    query = request.GET.get('q', '')  # Get search input safely
    if query:
        # Use ORM filter to prevent SQL injection
        books = Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )
    else:
        books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books, 'query': query})