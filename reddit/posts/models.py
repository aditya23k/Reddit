from django.db import models
from django.contrib.auth.models import User
from subreddits.models import Subreddit


# Create your models here.
# Post model

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    subreddit = models.ForeignKey(
        Subreddit, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    upvoted_by = models.ManyToManyField(User, related_name='upvoted_posts')
    downvoted_by = models.ManyToManyField(User, related_name='downvoted_posts')

    def __str__(self):
        return self.title

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
