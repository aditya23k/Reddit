
from django.urls import path
from . import views

app_name = 'subreddits'

urlpatterns = [
    path('create/', views.create_subreddit, name='create_subreddit'),
    path('<int:subreddit_id>/', views.view_subreddit, name='view_subreddit')

]
