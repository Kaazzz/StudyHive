from django.db import models
from django.contrib.auth.models import User 

# Create your models here.

class Post(models.Model):
    
    title = models.CharField(max_length=100)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    group_id = models.CharField(max_length=6, unique=True, blank=True)
    

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post,related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author} on {self.post.title}'   