from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Subreddit(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='created_subreddits')

    def __str__(self):
        return self.name
