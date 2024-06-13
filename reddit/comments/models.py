from django.db import models
from django.contrib.auth.models import User
from posts.models import Post
from django.utils import timezone


# Create your models here.
# Comment model

class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey(
        'self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)
    upvoted_by = models.ManyToManyField(
        User, related_name='upvoted_comments', blank=True)
    downvoted_by = models.ManyToManyField(
        User, related_name='downvoted_comments', blank=True)

    def __str__(self):
        return self.content

    def get_vote_count(self):
        return self.upvoted_by.count() - self.downvoted_by.count()

    def upvote(self, user):
        if user in self.downvoted_by.all():
            self.downvoted_by.remove(user)
        if user in self.upvoted_by.all():
            self.upvoted_by.remove(user)
        else:
            self.upvoted_by.add(user)

    def downvote(self, user):
        if user in self.upvoted_by.all():
            self.upvoted_by.remove(user)
        if user in self.downvoted_by.all():
            self.downvoted_by.remove(user)
        else:
            self.downvoted_by.add(user)
