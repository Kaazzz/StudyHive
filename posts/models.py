from django.db import models

# Create your models here.

class PostContent(models.Model):
    name = models.CharField(max_length=100)
    comment = models.TextField()


    def __str__(self):
        return self.name
    
class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author} on {self.post.title}'   