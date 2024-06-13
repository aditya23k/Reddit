from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()


class Follow(models.Model):
    follower = models.ForeignKey(
        User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(
        User, related_name='followers', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.follower} follows {self.following}"
