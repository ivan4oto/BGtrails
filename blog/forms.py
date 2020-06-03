from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Post, Adventurer


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class AdventurerForm(forms.ModelForm):
    class Meta:
        model = Adventurer
        fields = '__all__'
        exclude = ['user']


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'distance', 'elevation', 'description', 'file']
