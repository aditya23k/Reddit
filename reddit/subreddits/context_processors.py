# subreddits/context_processors.py
from .models import Subreddit


def subreddit_list(request):
    subreddits = Subreddit.objects.all()
    return {'subreddits': subreddits}
