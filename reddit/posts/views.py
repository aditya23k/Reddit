
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post
from comments.models import Comment
from subreddits.models import Subreddit
from django.http import JsonResponse
# Create your views here.


@login_required(login_url='login')
def create_post(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        subreddit_id = request.POST['subreddit']
        subreddit = get_object_or_404(Subreddit, pk=subreddit_id)
        post = Post(title=title, content=content,
                    author=request.user, subreddit=subreddit)
        post.save()
        messages.success(request, 'Post created successfully')
        return redirect('subreddits:view_subreddit', subreddit_id=subreddit_id)
    else:
        subreddit_id = request.GET.get('subreddit')
        subreddit = get_object_or_404(Subreddit, pk=subreddit_id)

        return render(request, 'posts/create_post.html', {'subreddit': subreddit})


def view_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        parent_comment_id = request.POST.get('parent_comment_id')
        parent_comment = None

        if parent_comment_id:
            parent_comment = get_object_or_404(Comment, id=parent_comment_id)

        if content:
            Comment.objects.create(
                post=post,
                author=request.user,
                content=content,
                parent_comment=parent_comment
            )
            messages.success(request, 'Comment added successfully')
        else:
            messages.error(request, 'Text field cannot be empty')

        return redirect('posts:view_post', post_id=post_id)

    comments = Comment.objects.filter(post=post, parent_comment__isnull=True).select_related(
        'author').prefetch_related('replies')

    return render(request, 'posts/view_post.html', {'post': post, 'comments': comments})


@login_required(login_url='login')
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.user != post.author:
        messages.error(request, 'You are not authorized to edit this post.')
        return redirect('posts:view_post', post_id=post_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        if title and content:
            post.title = title
            post.content = content
            post.save()
            messages.success(request, 'Post updated successfully')
            return redirect('posts:view_post', post_id=post_id)
        else:
            messages.error(request, 'Both title and content are required.')

    return render(request, 'posts/edit_post.html', {'post': post})


@login_required(login_url='login')
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.user != post.author:
        messages.error(request, 'You are not authorized to delete this post.')
        return redirect('posts:view_post', post_id=post_id)

    post.delete()
    messages.success(request, 'Post deleted successfully')
    return redirect('subreddits:view_subreddit', subreddit_id=post.subreddit.id)


@login_required(login_url='login')
def upvote_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.upvote(request.user)
    post.save()
    return JsonResponse({'vote_count': post.get_vote_count()})


@login_required(login_url='login')
def downvote_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.downvote(request.user)
    post.save()
    return JsonResponse({'vote_count': post.get_vote_count()})


@login_required(login_url='login')
def vote_post(request):
    post_id = request.POST.get('post_id')
    action = request.POST.get('action')
    post = get_object_or_404(Post, pk=post_id)
    if action == 'upvote':
        post.upvote(request.user)
    elif action == 'downvote':
        post.downvote(request.user)
    post.save()
    return JsonResponse({'vote_count': post.get_vote_count()})
