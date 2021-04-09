from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

# Create your views here.
from trails.models import Trail
from .forms import LoginForm, RegisterForm

User = get_user_model()

def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password1")
        password2 = form.cleaned_data.get("password2")
        try:
            user = User.objects.create_user(username, email, password)
        except:
            user = None
        if user != None:
            login(request, user)
            return redirect("/")
        else:
            request.session['register_error'] = 1 # 1 == True
    return render(request, "accounts/create_user.html", {"form": form})

def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user != None:
            # user is valid and active -> is_active
            # request.user == user
            login(request, user)
            return redirect("/")
        else:
            # attempt = request.session.get("attempt") or 0
            # request.session['attempt'] = attempt + 1
            # return redirect("/invalid-password")
            request.session['invalid_user'] = 1 # 1 == True
    return render(request, "accounts/login_user.html", {"form": form})

@login_required
def logout_view(request):
    logout(request)
    # request.user == Anon User
    return redirect("/")

def user_detail(request, username):
    user = User.objects.filter(username=username)

    return render(request, "trails/detail_trail.html", {"object": obj})

@login_required
def favourite_trail(request, pk):
    context = {}
    trail = get_object_or_404(Trail, pk=pk)
    user = request.user
    print('\n\n {} \n\n'.format(user.username))
    if trail in user.favourites.all():
        user.favourites.remove(trail)
    else:
        user.favourites.add(trail)
    return render(request, "home.html", context)

    