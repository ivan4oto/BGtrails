from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Post, Adventurer, Rate


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
    # image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Post
        fields = ['title', 'distance', 'elevation', 'description', 'file', 'author', 'image']


class RateForm(forms.ModelForm):
    class Meta:
        model = Rate
        fields = '__all__'
        exclude = ['author', 'post']
