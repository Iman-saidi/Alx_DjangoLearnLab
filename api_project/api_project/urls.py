# api_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

# Optional: a simple landing page at /
def home(request):
    return HttpResponse("<h1>Welcome to the A.D.Ai API</h1><p>Go to <a href='/api/'>/api/</a> to access the API.</p>")

urlpatterns = [
    path('', home),                         # http://127.0.0.1:8000/
    path('admin/', admin.site.urls),        # Admin
    path('api/', include('api.urls')),      # Your app-level URLs
]
