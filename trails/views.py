from django.shortcuts import render, redirect

from .forms import TrailForm
# Create your views here.


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
        return redirect("/success")
    return render(request, "create_trail.html", {"form": form})

