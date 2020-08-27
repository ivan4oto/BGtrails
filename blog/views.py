from django import forms
from django.contrib import messages
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Avg
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic import (
    CreateView
)
from measurement.measures import Distance

from coordinates import get_location, get_distance, get_track_length
from .decorators import allowed_users
from .forms import CreateUserForm, CreatePostForm, AdventurerForm, RateForm, ImagePostForm
from .models import Post, Adventurer, PostImage, Rate


def map_page(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post_gpx = staticfiles_storage.url(f'{post.file}')
    lat = post.lat
    lon = post.lon

    return render(request, 'blog/map.html', context={'post': post,
                                                     'postfile': post_gpx,
                                                     'lat': lat,
                                                     'lon': lon})


def register_page(request):
    if request.user.is_authenticated:
        return redirect('/blog/')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')

                group = Group.objects.get_or_create(name='adventurers')
                user.groups.add(group[0])
                Adventurer.objects.create(user=user, name=user.username)

                messages.success(request, 'Account was created for ' + username)

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


def not_logged_in(request):
    return render(request, 'blog/not_logged_in.html')


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    name = request.GET.get('name')
    distance = request.GET.get('distance')
    elevation = request.GET.get('elevation')
    u_lat = request.GET.get('lat')
    u_lon = request.GET.get('lon')
    radius = request.GET.get('radius')

    if radius and u_lat and u_lon:
        inrange_trails = [post.id for post in Post.objects.all() if post.in_range((u_lat, u_lon, ), radius)]
        el_query = Post.objects.filter(id__in=inrange_trails)

        context['posts'] = el_query
        return render(request, 'blog/post_list.html', context)
    if name:
        context['posts'] = Post.objects.filter(title__icontains=name)
        return render(request, 'blog/post_list.html', context)
    if distance:
        context['posts'] = Post.objects.filter(distance__gt=Distance(km=distance))
        return render(request, 'blog/post_list.html', context)
    if elevation:
        context['posts'] = Post.objects.filter(elevation__gt=Distance(m=elevation))
        return render(request, 'blog/post_list.html', context)

    return render(request, 'blog/post_list.html', context)


@login_required(login_url='blog:login')
@allowed_users(allowed_roles=['adventurers', 'admin'])
def adventurer(request, pk_adventurer):
    adventurer = Adventurer.objects.get(id=pk_adventurer)
    """
    vceki post e svarzan s adventurer a ne s usera(ot Django)
    a adventurer e svarzan s usara na Django
    """
    posts = Post.objects.filter(author=adventurer)
    posts_count = posts.count()

    context = {'adventurer': adventurer, 'posts': posts, 'posts_count': posts_count}
    return render(request, 'blog/adventurer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['adventurers', 'admin'])
def account_settings(request):
    adventurer = request.user.adventurer
    form = AdventurerForm(instance=adventurer)

    if request.method == 'POST':
        form = AdventurerForm(request.POST, request.FILES, instance=adventurer)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'blog/adventurer_settings.html', context)


def detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    photos = PostImage.objects.filter(post=post)
    return render(request, 'blog/detail.html', {
        'post': post,
        'photos': photos
    })


# def upload_image_view(request):
#     user = request.user
#     print(request)
#     if request.method == 'POST':
#         file_form = ImagePostForm(request.POST, request.FILES)
#         files = request.FILES.getlist('image') #field name in model
#         if file_form.is_valid():
#             feed_instance = form.save(commit=False)
#             feed_instance.user = user
#             feed_instance.save()
#             for f in files:
#                 file_instance = FeedFile(file=f, feed=feed_instance)
#                 file_instance.save()
#     else:
#         form = FeedModelForm()
#         file_form = FileModelForm()


class ImageFieldView(FormView):
    model = PostImage
    form_class = ImagePostForm
    template_name = 'blog/add_photos.html'
    success_url = reverse_lazy('blog-home')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('image')
        if form.is_valid():
            post_id = int(request.build_absolute_uri('?').split('/')[-2])
            for f in files:
                post_instance = Post.objects.get(pk=post_id)
                image_instance = PostImage(post=post_instance, image=f)
                image_instance.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class PostCreateView(CreateView):
    model = Post
    form_class = CreatePostForm
    queryset = Post.objects.all()

    def form_valid(self, form, coordinates, username, distance, elevation, *args, **kwargs):
        response = super().form_valid(form=form, *args, **kwargs)
        self.object.lat = coordinates[0]
        self.object.lon = coordinates[1]
        self.object.distance = distance
        self.object.elevation = elevation
        self.object.author = username
        self.object = form.save()
        return response

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = CreatePostForm(request.POST, request.FILES)
            images = request.FILES.getlist('image_field')

            if form.is_valid():
                gpx = str(form.cleaned_data.get('file').read(1024))
                form.cleaned_data.get('file').seek(0)
                gpxFile = form.cleaned_data.get('file')
                coordinates = get_location(gpx)
                """ Parse gpx to get distance and elevation """
                distance, elevation = get_track_length(gpxFile)
                distance = Distance(km=distance)
                elevation = Distance(m=elevation)

                return self.form_valid(form=form, coordinates=coordinates, username=request.user.adventurer,
                                       elevation=elevation, distance=distance)
            else:
                return self.form_invalid(form=form)
        else:
            return redirect(reverse('not-logged-in'))


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'distance', 'elevation', 'description', 'image']


@login_required(login_url='login')
@allowed_users(allowed_roles=['adventurers', 'admin'])
def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)
    adventurer = request.user.adventurer
    if not Post.objects.filter(author=adventurer):
        return redirect('blog-home')

    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect(reverse('blog-home'))
        else:
            return render(request, 'blog/edit_post.html', {'post': post, 'form': form})
    else:
        form = CreatePostForm(instance=post)
        return render(request, 'blog/edit_post.html', {'post': post, 'form': form})


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


@login_required(login_url='login')
@allowed_users(allowed_roles=['adventurers', 'admin'])
def rate(request, post_id):
    form = RateForm()
    post = Post.objects.get(id=post_id)
    adventurer = request.user.adventurer

    rate_already = Rate.objects.filter(post_id=post_id).filter(author=adventurer).count()
    if rate_already != 0:
        messages.success(request, 'You already rate this post!!')
        return redirect(reverse('blog-home'))

    if request.method == 'POST':
        form = RateForm(request.POST)
        if form.is_valid():
            rating = form.save()
            rating.author = adventurer
            rating.post = post
            rating.save()
            return redirect(reverse('blog-home'))

    context = {'form': form}
    return render(request, 'blog/rate.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['adventurers', 'admin'])
def want_go(request):
    adventurer = request.user.adventurer
    posts = Post.objects.filter(want_go=adventurer)
    posts_count = posts.count()

    context = {'adventurer': adventurer, 'posts': posts, 'posts_count': posts_count}
    return render(request, 'blog/want_go.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['adventurers', 'admin'])
def add_post(request, post_id):
    adventurer = request.user.adventurer
    posts = Post.objects.filter(id=post_id)[0]
    posts.want_go.add(adventurer)

    return redirect('want-go')


@login_required(login_url='login')
@allowed_users(allowed_roles=['adventurers', 'admin'])
def went_there(request):
    adventurer = request.user.adventurer
    posts = Post.objects.filter(been_there=adventurer)
    posts_count = posts.count()

    context = {'adventurer': adventurer, 'posts': posts, 'posts_count': posts_count}
    return render(request, 'blog/been_there.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['adventurers', 'admin'])
def add_been_there(request, post_id):
    adventurer = request.user.adventurer
    posts = Post.objects.filter(id=post_id)[0]
    posts.been_there.add(adventurer)

    return redirect('went_there')


@login_required(login_url='login')
@allowed_users(allowed_roles=['adventurers', 'admin'])
def remove_from_wanted(request, post_id):
    adventurer = request.user.adventurer
    posts = Post.objects.filter(id=post_id)[0]
    posts.want_go.remove(adventurer)

    return redirect('want-go')


def reviews(request, post_id):
    post = Post.objects.filter(id=post_id).first()
    count_wand_to_go = post.want_go.count()
    count_been_there = post.been_there.count()
    rates = Rate.objects.filter(post_id=post_id)
    average = rates.all().aggregate(Avg('rate'))

    context = {'rates': rates, 'average': average['rate__avg'], 'been_there': count_been_there,
               'want_go': count_wand_to_go}
    return render(request, 'blog/review.html', context)
