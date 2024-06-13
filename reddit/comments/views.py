from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Comment
from .forms import CommentForm
from posts.models import Post
from django.http import JsonResponse

# Create your views here.


@login_required(login_url='login')
def add_comment_to_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('posts:view_post', post_id=post.id)
    else:
        form = CommentForm()
    return render(request, 'comments/add_comment_to_post.html', {'form': form})


@login_required(login_url='login')
def reply_to_comment(request, comment_id):
    parent_comment = get_object_or_404(Comment, id=comment_id)
    post = parent_comment.post
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.parent_comment = parent_comment
            reply.post = post
            reply.save()
            return redirect('posts:view_post', post_id=post.id)
    else:
        form = CommentForm()
    return render(request, 'comments/reply_to_comment.html', {'form': form})


@login_required(login_url='login')
def upvote_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user not in comment.upvoted_by.all():
        comment.upvoted_by.add(request.user)
        comment.downvoted_by.remove(request.user)
        comment.save()
        messages.success(request, 'Comment upvoted successfully.')
    else:
        messages.warning(request, 'You have already upvoted this comment.')

    return redirect(request.META.get('HTTP_REFERER', 'posts:view_post', args=[comment.post.id]))


@login_required(login_url='login')
def downvote_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user not in comment.downvoted_by.all():
        comment.downvoted_by.add(request.user)
        comment.upvoted_by.remove(request.user)
        comment.save()
        messages.success(request, 'Comment downvoted successfully.')
    else:
        messages.warning(request, 'You have already downvoted this comment.')

    return redirect(request.META.get('HTTP_REFERER', 'posts:view_post', args=[comment.post.id]))
