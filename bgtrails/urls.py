"""bgtrails URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.contrib import admin
from django.urls import path
from trails.views import trail_create_view, trail_detail_view, home_view, trail_delete_view, trail_type_view, about_view, trail_update_view
from accounts.views import register_view, login_view, logout_view, favourite_trail, user_detail
# from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('about', about_view, name='about'),
    path('create-trail', trail_create_view, name='create-trail'),
    path('delete-trail/<int:pk>/', trail_delete_view, name='delete-trail'),
    path('detail-trail/<int:pk>/', trail_detail_view, name='detail-trail'),
    path('update-trail/<int:pk>/', trail_update_view, name='update-trail'),
    path('type-trail/<str:tag>/', trail_type_view, name='type-trail'),
    path('register', register_view, name='register'),
    path(settings.LOGIN_URL, login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('user/<str:username>/', user_detail, name='user-detail'),
    path('favourite-trail/<int:pk>/', favourite_trail, name='favourite-trail')
]


# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

