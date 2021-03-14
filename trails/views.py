from django.shortcuts import render, redirect
from django.http import Http404

from .forms import TrailForm
from .models import Trail
from .filters import TrailFilter
# Create your views here.


def home_view(request, *args, **kwargs):
    objs = Trail.objects.all() # [obj1, obj2, obj3,]
    myFilter = TrailFilter(request.GET, queryset=objs)

    context = {"object_list": objs, "myFilter": myFilter}
    return render(request, "home.html", context)


def trail_create_view(request):
    form = TrailForm(request.POST or None, request.FILES or None)
    print('before form check')
    if form.is_valid():
        print('before form save')
        obj = form.save(commit=False)
        print('after form save')
        gpx_file = request.FILES.get('gpx_file')
        print(request.FILES)
        print(gpx_file, ' <------ gpx file --------')
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