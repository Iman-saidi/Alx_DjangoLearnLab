from django_filters import rest_framework as filters  # Add this import
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Book, Story, UserProfile, Workshop
from .serializers import BookSerializer, StorySerializer, UserProfileSerializer, WorkshopSerializer

# Add these filter classes
class BookFilter(filters.FilterSet):
    class Meta:
        model = Book
        fields = {
            'title': ['exact', 'icontains'],
            'author__username': ['exact'],
            'published_date': ['exact', 'year__gt', 'year__lt'],
        }

class WorkshopFilter(filters.FilterSet):
    class Meta:
        model = Workshop
        fields = {
            'title': ['exact', 'icontains'],
            'host__username': ['exact'],
            'start_date': ['exact', 'gt', 'lt'],
        }

# ViewSets with filtering support
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related('author')
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.DjangoFilterBackend]  # Add filter backend
    filterset_class = BookFilter  # Add filterset class

class WorkshopViewSet(viewsets.ModelViewSet):
    queryset = Workshop.objects.select_related('host').prefetch_related('stories')
    serializer_class = WorkshopSerializer
    filter_backends = [filters.DjangoFilterBackend]  # Add filter backend
    filterset_class = WorkshopFilter  # Add filterset class

# ... (keep your existing StoryViewSet and UserProfileViewSet)

# Update specialized views with filtering
class PublishedBooksList(generics.ListAPIView):
    """List view for published books with custom filtering"""
    serializer_class = BookSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = BookFilter
    
    def get_queryset(self):
        return Book.objects.filter(published_date__isnull=False)

class WorkshopStoriesList(generics.ListCreateAPIView):
    """List/Create stories for a specific workshop"""
    serializer_class = StorySerializer
    
    def get_queryset(self):
        workshop_id = self.kwargs['workshop_id']
        return Story.objects.filter(workshop_id=workshop_id)
    
class BookList(generics.ListAPIView):
    """List view for all books"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = BookFilter
