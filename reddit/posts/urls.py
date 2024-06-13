from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('create/', views.create_post, name='create_post'),
    path('<int:post_id>/', views.view_post, name='view_post'),
    path('edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('vote/', views.vote_post, name='vote_post'),

]
