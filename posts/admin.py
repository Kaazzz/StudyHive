from django.contrib import admin
from .models import PostContent, Post, Comment

# Register your models here.
admin.site.register(PostContent)
admin.site.register(Post)
admin.site.register(Comment)