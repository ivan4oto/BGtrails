from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView
)

from django import forms
from .forms import CreateUserForm, CreatePostForm
from .models import Post, PostImage
from django.contrib import messages

from measurement.measures import Distance


def register_page(request):
    if request.user.is_authenticated:
        return redirect('/blog/')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('login')

        context = {'form': form}
        return render(request, 'blog/register.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('blog-home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'blog/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('/blog/')


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    name = request.GET.get('name')
    distance = request.GET.get('distance')
    elevation = request.GET.get('name')
    if name:
        context['posts'] = Post.objects.filter(title__icontains=name)
        return render(request, 'blog/post_list.html', context)
    if distance:
        context['posts'] = Post.objects.filter(distance__gt=Distance(km=distance))
        return render(request, 'blog/post_list.html', context)
    if elevation:
        context['posts'] = Post.objects.filter(distance__gt=Distance(m=elevation))
        return render(request, 'blog/post_list.html', context)

    return render(request, 'blog/post_list.html', context)


def detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    photos = PostImage.objects.filter(post=post)
    return render(request, 'blog/detail.html', {
        'post': post,
        'photos': photos
    })


# class PostListView(ListView):
#     queryset = Post.objects.all()


# class PostDetailView(DetailView):

#     def get_object(self):
#         id_ = self.kwargs.get("post_id")
#         return get_object_or_404(Post, id=id_)


class PostCreateView(CreateView):
    model = Post
    form_class = CreatePostForm
    queryset = Post.objects.all()


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'distance', 'elevation', 'description', 'image']


def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = PostForm(data=request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect(reverse('blog-home'))
        else:
            return render(request, 'blog/edit_post.html', {'post': post, 'form': form})
    else:
        form = PostForm(instance=post)
        return render(request, 'blog/edit_post.html', {'post': post, 'form': form})


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
