from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Subreddit
from django.contrib import messages


# Create your views here.

@login_required(login_url='/login/')
def create_subreddit(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        description = request.POST.get('description')

        if Subreddit.objects.filter(name=name).exists():
            messages.info(request, 'Subreddit name taken')
            return render(request, 'subreddits/create_subreddit.html')

        else:
            subreddit = Subreddit.objects.create(
                name=name, description=description, creator=request.user)
            subreddit.save()
            messages.info(request, 'Subreddit created')
            return redirect('reddit_users:index')

    else:
        return render(request, 'subreddits/create_subreddit.html')


def view_subreddit(request, subreddit_id):
    subreddit = Subreddit.objects.get(id=subreddit_id)
    posts = subreddit.posts.all()
    return render(request, 'subreddits/view_subreddit.html', {'subreddit': subreddit, 'posts': posts})
