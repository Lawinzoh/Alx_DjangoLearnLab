from time import timezone
from api_project.api import serializers
from .models import Book, Author


# AuthorSerializer converts Author model instances into JSON format and back.
# It includes the author's name and a nested list of related books.
# The "books" field is populated using the BookSerializer defined above.
        # 'books' leverages the related_name="books" in the Book model,
    # which enables reverse lookup of all books linked to an Author.
class AuthorSerializer(serializers.ModelSerializer):
    books = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Author
        fields = '__all__'


# BookSerializer converts Book model instances into JSON format and back.
# It includes all fields of the Book model and enforces validation rules.
class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    
    # W: For write operations (POST, PUT, PATCH), require the author's ID
    # This field is write_only and targets the 'author' field on the Book model
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), 
        source='author', # Maps the validated ID back to the 'author' field on the Book model
        write_only=True  # Excludes this field from the GET response
    )

    class Meta:
        model = Book
        fields = '__all__  '
    

    # Custom validation ensures that the publication year is not set in the future.
    def validate_publication_year(self, value):
        current_year = timezone.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

