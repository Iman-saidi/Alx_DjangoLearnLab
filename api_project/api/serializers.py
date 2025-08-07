from rest_framework import serializers
from .models import Book, Workshop, Story, UserProfile, Author
from datetime import datetime
from django.contrib.auth.models import User

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'bio']

class BookSerializer(serializers.ModelSerializer):
    # Nested author representation instead of just ID
    author = AuthorSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        source='author',
        write_only=True
    )
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'author_id', 'published_date', 'isbn']
    
    def validate_published_date(self, value):
        """Ensure publication date isn't in the future"""
        if value and value.year > datetime.now().year:
            raise serializers.ValidationError("Publication year cannot be in the future")
        return value

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'role', 'points', 'bio']
        read_only_fields = ['points']

class WorkshopSerializer(serializers.ModelSerializer):
    # Nested host profile
    host = UserProfileSerializer(read_only=True)
    host_id = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.all(),
        source='host',
        write_only=True
    )
    
    # Nested stories count
    stories_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Workshop
        fields = '__all__'
        extra_kwargs = {
            'latitude': {'required': True},
            'longitude': {'required': True}
        }
    
    def get_stories_count(self, obj):
        return obj.stories.count()

class StorySerializer(serializers.ModelSerializer):
    # Nested author profile
    author = UserProfileSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.all(),
        source='author',
        write_only=True,
        required=False,
        allow_null=True
    )
    
    class Meta:
        model = Story
        fields = '__all__'
        read_only_fields = ['submitted_at']
