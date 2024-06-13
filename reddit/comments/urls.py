from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('post/<int:post_id>/comment/',
         views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:comment_id>/reply/',
         views.reply_to_comment, name='reply_to_comment'),
    path('comment/<int:comment_id>/upvote/',
         views.upvote_comment, name='upvote_comment'),
    path('comment/<int:comment_id>/downvote/',
         views.downvote_comment, name='downvote_comment'),

]
