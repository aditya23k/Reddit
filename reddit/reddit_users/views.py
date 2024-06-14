from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import RedditUser
from posts.models import Post
from comments.models import Comment
from follow.models import Follow
from subreddits.models import Subreddit
from django.http import JsonResponse
from django.db.models import Q


# Create your views here.


def index(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'reddit_users/homepage.html', {'posts': posts})


def follower_count(username):
    user = get_object_or_404(User, username=username)
    followers = Follow.objects.filter(following=user).count()
    return followers


def following_count(username):
    user = get_object_or_404(User, username=username)
    following = Follow.objects.filter(follower=user).count()
    return following


def view_profile(request, username):
    user = get_object_or_404(User, username=username)
    reddit_user = get_object_or_404(RedditUser, user=user)
    posts = Post.objects.filter(author=user).order_by('-created_at')
    comments = Comment.objects.filter(author=user).order_by('-created_at')
    post_count = posts.count()
    comment_count = Comment.objects.filter(author=user).count()
    is_following = Follow.objects.filter(
        follower=request.user, following=user).exists() if request.user.is_authenticated else False
    count_following = following_count(username=user.username)
    count_follower = follower_count(username=user.username)
    return render(request, 'reddit_users/profile.html', {
        'reddit_user': reddit_user,
        'posts': posts,
        'comments': comments,
        'profile_user': user,
        'post_count': post_count,
        'comment_count': comment_count,
        'is_following': is_following,
        'following_count': count_following,
        'follower_count': count_follower
    })


@login_required(login_url='/login/')
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    follow, created = Follow.objects.get_or_create(
        follower=request.user, following=user_to_follow)
    if created:
        messages.info(request, f'You are now following {user_to_follow}')
    else:
        follow.delete()
        messages.info(request, f'You are no longer following {user_to_follow}')

    return redirect('reddit_users:view_profile', username=username)


@login_required(login_url='/login/')
def unfollow_user(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    follow = Follow.objects.filter(
        follower=request.user, following=user_to_unfollow).delete()
    messages.info(request, f'You are no longer following {user_to_unfollow}')

    return redirect('reddit_users:view_profile', username=username)


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username taken')
                return render(request, 'reddit_users/signup.html')

            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email taken')
                return render(request, 'reddit_users/signup.html')
            else:
                user = User.objects.create_user(
                    username=username, password=password, email=email)
                user.save()

                user_model = User.objects.get(username=username)
                reddit_user_model = RedditUser.objects.create(
                    user=user_model, id_user=user_model.id, email=email)
                reddit_user_model.save()
                messages.info(request, 'User and profile created')
                return redirect('reddit_users:login')
        else:
            messages.info(request, 'Passwords do not match')
            return render(request, 'reddit_users/signup.html')

    else:
        return render(request, 'reddit_users/signup.html')


def login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        print(user)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid credentials')
            return render(request, 'reddit_users/login.html')

    else:
        return render(request, 'reddit_users/login.html')


@login_required(login_url='/login/')
def logout(request):
    auth.logout(request)
    return redirect('reddit_users:index')


def search(request):
    query = request.GET.get('query')

    subreddits = Subreddit.objects.filter(name__icontains=query)
    users = User.objects.filter(username__icontains=query)
    posts = Post.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query))
    # print(f"Subreddits: {subreddits}")
    # print(f"Users: {users}")
    # print(f"Posts: {posts}")
    results = {
        'subreddits': [{'id': subreddit.id, 'name': subreddit.name} for subreddit in subreddits],
        'users': [{'username': user.username} for user in users],
        'posts': [{'id': post.id, 'title': post.title, 'author': post.author.username} for post in posts]
    }
    print(results)
    return JsonResponse(results)
