from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Post


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'distance', 'elevation', 'description', 'file']
