from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .forms import TrailForm
from .models import Trail
from .filters import TrailFilter
# Create your views here.


def home_view(request, *args, **kwargs):
    objs = Trail.objects.all() # [obj1, obj2, obj3,]
    myFilter = TrailFilter(request.GET, queryset=objs)
    user = request.user
    favourtes = user.favourites.all()
    context = {"object_list": objs, "myFilter": myFilter, "user_favs": favourtes}
    return render(request, "home.html", context)


@login_required
def trail_create_view(request):
    form = TrailForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        gpx_file = request.FILES.get('gpx_file')
        #do some stuff
        if gpx_file:
            obj.gpx_file = gpx_file
        obj.user = request.user
        obj.save()
        form = TrailForm()
        return redirect(to='home')
    return render(request, "trails/create_trail.html", {"form": form})


def trail_detail_view(request, pk):
    # obj = Trail.objects.get(id=id)
    try:
        obj = Trail.objects.get(pk=pk)
    except Trail.DoesNotExist:
        raise Http404 # render html page, with HTTP status code of 404
    return render(request, "trails/detail_trail.html", {"object": obj})

def trail_delete_view(request, pk):
    try:
        obj = Trail.objects.get(pk=pk)
    except Trail.DoesNotExist:
        raise Http404 # render html page, with HTTP status code of 404
    if request.user.has_perm('trails.delete_trail') or request.user == obj.user:
        obj.delete()
        data = {"error": False, "response": "Trail Deleted Successfully"}
        return redirect(to='home')