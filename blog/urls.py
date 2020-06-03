from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_page, name="register"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('', view=views.home, name='blog-home'),
    path('adventurer/<str:pk_adventurer>/', views.adventurer, name="adventurer"),
    path('edit/', views.account_settings, name="edit"),
    path('create/', view=views.PostCreateView.as_view(), name='create'),
    path('about/', view=views.about, name='blog-about'),
    path('update/<int:post_id>/', views.edit_post, name='update'),
    path('<int:post_id>/', views.detail, name='detail'),
]
