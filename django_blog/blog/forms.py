from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Comment, Post
from taggit.forms import TagWidget

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("bio", "avatar")
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4, "placeholder": "Tell something about yourself..."}),
        }


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
        
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment...'}),
        }
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']  # include tags
        widgets = {
            'tags': TagWidget(),  # allows multiple tags input
        }
