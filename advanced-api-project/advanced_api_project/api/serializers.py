from rest_framework import serializers
from .models import Book, Author
from datetime import datetime

# This file defines the serializers for the API project.
class BookSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'publication_year']  


    # This is a custom validation to Validate publication year to ensure it's a positive integer and not in the future
    def validate_publication_year(self, value):
        current_year = datetime.now().year
        if value < 0 or value > current_year:
            raise serializers.ValidationError("Publication year must be a positive integer and not in the future.")
        return value
       

class AuthorSerializer(serializers.ModelSerializer):
    # This is a nested serializer to include related books in the Author representation
    books = BookSerializer(many=True, read_only=True)  # Nested serializer for related books
    class Meta:
        model = Author
        fields = ['id', 'name', 'books'] # Include 'id' for unique identification  
