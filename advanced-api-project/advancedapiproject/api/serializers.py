from time import timezone
from api_project.api import serializers
from advanced_api_project.api.models import Book, Author


# BookSerializer converts Book model instances into JSON format and back.
# It includes all fields of the Book model and enforces validation rules.
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__  '
    

    # Custom validation ensures that the publication year is not set in the future.
    def validate_publication_year(self, value):
        current_year = timezone.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value


# AuthorSerializer converts Author model instances into JSON format and back.
# It includes the author's name and a nested list of related books.
# The "books" field is populated using the BookSerializer defined above.
        # 'books' leverages the related_name="books" in the Book model,
    # which enables reverse lookup of all books linked to an Author.
class AuthorSerializer(serializers.ModelSerializer):
    bokks = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = '__all__'