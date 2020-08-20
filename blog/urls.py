from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_page, name="register"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('not-logged-in/', views.not_logged_in, name="not-logged-in"),

    path('', view=views.home, name='blog-home'),
    path('rate/<int:post_id>/', views.rate, name="rate"),
    path('want-go/', views.want_go, name="want-go"),
    path('remove-want/<int:post_id>/', views.remove_from_wanted, name="remove-want"),
    path('went_there/', views.went_there, name="went_there"),
    path('add-post/<int:post_id>/', views.add_post, name="add-post"),
    path('add_been_there/<int:post_id>/', views.add_been_there, name="add_been_there"),
    path('reviews/<int:post_id>/', views.reviews, name="reviews"),

    path('adventurer/<str:pk_adventurer>/', views.adventurer, name="adventurer"),
    path('edit/', views.account_settings, name="edit"),
    path('create/', view=views.PostCreateView.as_view(), name='create'),
    path('about/', view=views.about, name='blog-about'),
    path('update/<int:post_id>/', views.edit_post, name='update'),
    path('add-photos/<int:post_id>/', views.ImageFieldView.as_view(), name='add-photos'),
    path('<int:post_id>/', views.detail, name='detail'),

    path('map/<int:post_id>/', views.map_page, name="map"),
]
