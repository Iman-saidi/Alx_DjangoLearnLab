from django.shortcuts import render

from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from .models import Book  # Needed for list_books view
from .models import Library  # Required for the check (even if Library is already used elsewhere)
from django.http import HttpResponseForbidden
from .models import UserProfile

@login_required
def admin_view(request):
    if request.user.userprofile.role == 'Admin':
        return render(request, 'relationship_app/admin_view.html')  # You can replace this with any template
    else:
        return HttpResponseForbidden("You do not have permission to access this page.")


def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'


@user_passes_test(is_admin)
def admin_view(request):
    return HttpResponse("Welcome, Admin!")

@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'librarian_view.html')

@user_passes_test(is_member)
def member_view(request):
    return render(request, 'member_view.html')





@user_passes_test(is_librarian)
def librarian_view(request):
    return HttpResponse("Welcome, Librarian!")

@user_passes_test(is_member)
def member_view(request):
    return HttpResponse("Welcome, Member!")


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # logs the user in after successful registration
            return redirect('library_list')  # or wherever you'd like to redirect
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})



# Function-based view to list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})


from django.views.generic.detail import DetailView

# Class-based view to display library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
