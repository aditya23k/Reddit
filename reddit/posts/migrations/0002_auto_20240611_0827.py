# Generated by Django 2.2.28 on 2024-06-11 08:27

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='downvoted_by',
            field=models.ManyToManyField(related_name='downvoted_posts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='upvoted_by',
            field=models.ManyToManyField(related_name='upvoted_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]