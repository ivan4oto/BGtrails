from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
import json
from .services import TrailServiceHelper
from .forms import TrailForm, TrailUpdateForm
from .models import Trail
from .filters import TrailFilter

def home_view(request, *args, **kwargs):
    objs = Trail.objects.all()
    myFilter = TrailFilter(request.GET, queryset=objs)
    user = request.user
    if user.is_authenticated:
        favourites = user.favourites.all()
    else:
        favourites = []
    context = {"object_list": objs, "myFilter": myFilter, "user_favs": favourites}
    return render(request, "home.html", context)

def trail_type_view(request, tag):
    objs = Trail.objects.filter(tag=tag)
    user = request.user
    myFilter = TrailFilter(request.GET, queryset=objs)
    if user.is_authenticated:
        favourites = user.favourites.all()
    else:
        favourites = []
    context = {"object_list": objs, "myFilter": myFilter, "user_favs": favourites}
    return render(request, "home.html", context)

@login_required
def trail_create_view(request):
    form = TrailForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        gpx_file = request.FILES.get('gpx_file')

        trail_object = TrailServiceHelper().create_trail(
            name=form.cleaned_data.get('name'),
            description=form.cleaned_data.get('description'),
            distance=form.cleaned_data.get('distance'),
            elevation=form.cleaned_data.get('elevation'),
            gpx_file=gpx_file,
            user=request.user,
            tag=form.cleaned_data.get('tag')
        )
        form = TrailForm(None, instance=trail_object)
        return render(request, "trails/detail_trail.html", {"object": trail_object, "form": form})
    
    return render(request, "trails/create_trail.html", {"form": form})


def trail_detail_view(request, pk):
    try:
        obj = Trail.objects.get(pk=pk)
    except Trail.DoesNotExist:
        raise Http404
    return render(request, "trails/detail_trail.html", {"object": obj})

@login_required
def trail_update_view(request, pk):
    if request.method == 'POST':
        try:
            obj = Trail.objects.get(pk=pk)
        except Trail.DoesNotExist:
            raise Http404
        trail_data = {
            'name': request.POST.get('trail_name'),
            'distance': request.POST.get('trail_distance'),
            'elevation': request.POST.get('trail_elevation'),
            'description': request.POST.get('trail_description')
            }
        response_data = {}
        form = TrailUpdateForm(trail_data or None, instance=obj)
        if form.is_valid():
            TrailServiceHelper().update_trail(
                form=form.cleaned_data,
                pk=pk
                )
            response_data['result'] = 'Create post successful!'
        else:
            print(form.errors)
            response_data['result'] = 'Create post NOT succesful'

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


def trail_delete_view(request, pk):
    try:
        obj = Trail.objects.get(pk=pk)
    except Trail.DoesNotExist:
        raise Http404 # render html page, with HTTP status code of 404
    if request.user.has_perm('trails.delete_trail') or request.user == obj.user:
        obj.delete()
        data = {"error": False, "response": "Trail Deleted Successfully"}
        return redirect(to='home')

def about_view(request):
    return render(request, 'about.html')