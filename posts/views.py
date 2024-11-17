from django.shortcuts import render,redirect, get_object_or_404
from .models import Post
from .forms import PostForm,CommentForm
from django.contrib.auth.decorators import login_required
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
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False) 

            comment.post = post  
            comment.user = request.user  
            comment.save()
            return redirect('post')  
    else:
        form = CommentForm()

    return render(request, 'comment_post.html', {'form': form, 'post': post})