from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class RedditUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_user = models.IntegerField(max_length=10)
    password = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return self.user.username
