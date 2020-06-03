from django.http import HttpResponse


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = set([i.name for i in request.user.groups.all()])

            if any(i in group for i in allowed_roles):
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')

        return wrapper_func

    return decorator
