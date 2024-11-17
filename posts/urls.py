from django.urls import path
from . import views

urlpatterns = [
    path('', views.Posts, name='post'),
    path('create_post', views.Create_Post, name='create_post'),
    path('<int:post_id>/comment/', views.comment_post, name='comment_post'),
    
]
