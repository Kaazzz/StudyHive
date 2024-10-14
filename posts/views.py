from django.shortcuts import render,redirect
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required
# Create your views here.


def index(request):
    return render(request, 'post.html')




@login_required
def index(request):
    return render(request, 'post.html')

def Posts(request):
    posts = Post.objects.all()
    return render(request, 'post.html', {'posts': posts})
    

def Post_list(request):
    posts = Post.objects.all()
    return render(request, 'post_list.html', {'posts': posts})




def Create_Post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('post')  
    else:
        form = PostForm()

    return render(request, 'create_post.html', {'form': form})