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