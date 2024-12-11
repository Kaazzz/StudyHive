from django.shortcuts import render,redirect, get_object_or_404
from .models import Post, Comment
from .forms import PostForm,CommentForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# Create your views here.

def Posts(request):
    posts = Post.objects.all()
    return render(request, 'post.html', {'posts': posts})

def Create_Post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()  
            return redirect('post')  
    else:
        form = PostForm()

    return render(request, 'create_post.html', {'form': form})

def comment_post(request, post_id):
    post_comment = get_object_or_404(Post, pk=post_id)
    posts = Post.objects.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False) 

            comment.post = post_comment 
            comment.author = request.user  
            comment.save()
            return redirect('post')  
    else:
        form = CommentForm()

    return render(request, 'comment_post.html', {'form': form, 'pc': post_comment, 'posts': posts})


def TW(request):
    
    return render(request, 'posts/TW.html')

def delete_post(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(pk=post_id)
        post.delete()
        return redirect('post')  # Redirect to your desired page

    return render(request, 'post.html')

def delete_comment(request, comment_id):
    if request.method == 'POST':
        comment = Comment.objects.get(pk=comment_id)
        comment.delete()
        return redirect('post')  # Redirect to the post's detail page or a list of comments

    return render(request, 'post.html', {'comment': comment})

def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    # Check if the user is authorized to edit the post
    if request.user != post.author:
        return HttpResponse("You are not authorized to edit this post.")

    if request.method == 'POST':
        # Update the existing post instance with form data
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post') 
    else:
        # Pre-populate the form with existing post data
        form = PostForm(instance=post)

    return render(request, 'edit_post.html', {'form': form, 'post': post})


def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    # Check if the user is authorized to edit the comment (e.g., only the author)
    if request.user != comment.author:
        return HttpResponse("You are not authorized to edit this comment.")

    if request.method == 'POST':
        # Update the existing comment instance with form data
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post')  # Redirect to the post's detail page
    else:
        # Pre-populate the form with existing comment data
        form = CommentForm(instance=comment)

    return render(request, 'edit_comment.html', {'form': form, 'comment': comment})