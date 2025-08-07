# api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorkshopViewSet, StoryViewSet, UserProfileViewSet, BookList  # Added BookList
from django.http import JsonResponse

router = DefaultRouter()
router.register('workshops', WorkshopViewSet)
router.register('stories', StoryViewSet)
router.register('profile', UserProfileViewSet)

# Optional API root endpoint
def api_root(request):
    return JsonResponse({
        "message": "Welcome to the ADAi API",
        "workshops": "/api/workshops/",
        "stories": "/api/stories/",
        "profiles": "/api/profile/",
        "books": "/api/books/"  # Added books endpoint
    })

urlpatterns = [
    path('', api_root),               # http://127.0.0.1:8000/api/
    path('books/', BookList.as_view(), name='book-list'),  # Added BookList endpoint
    path('', include(router.urls)),  # /api/workshops/, etc.
]
