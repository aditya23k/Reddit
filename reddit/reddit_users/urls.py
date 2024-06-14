
from django.urls import path
from . import views

app_name = 'reddit_users'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/<str:username>/', views.view_profile, name='view_profile'),
    path('profile/<str:username>/follow/',
         views.follow_user, name='follow_user'),
    path('profile/<str:username>/unfollow/',
         views.unfollow_user, name='unfollow_user'),
    path('search/', views.search, name='search')
]
