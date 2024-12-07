from django.urls import path
from . import views

urlpatterns = [
    path('', views.Posts, name='post'),
    path('create_post', views.Create_Post, name='create_post'),
    path('<int:post_id>/comment/', views.comment_post, name='comment_post'),
    path('TW', views.TW, name='Tailwind'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
]
