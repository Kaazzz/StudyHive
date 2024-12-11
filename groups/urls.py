from django.urls import path
from .views import profile_view
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('create/', views.create_group, name='create_group'),
    path('join/', views.join_group, name='join_group'),
    path('profile/', profile_view, name='profile'),
    path('home_page/', views.home_page, name='home_page'),
    
    path('search_groups/', views.search_groups, name='search_groups'),
    path('request_join/', views.request_join, name='request_join'),
   
    path('group/<str:unique_id>/members/', views.group_members, name='group_members'),
    path('group/<str:unique_id>/remove/<int:member_id>/', views.remove_member, name='remove_member'),

    path('groups/<str:unique_id>/', views.group_dashboard, name='group_dashboard'),

    path('group/<str:unique_id>/requests/', views.group_requests, name='group_requests'),
    path('group/<str:unique_id>/accept_request/<int:join_request_id>/', views.accept_request, name='accept_request'),
    path('group/<str:unique_id>/reject_request/<int:join_request_id>/', views.reject_request, name='reject_request'),
    
    path('group/<str:group_id>/group_files/', views.group_files_view, name='group_files'),
    path('delete_file/<str:group_id>/<int:file_id>/', views.delete_file, name='delete_file'),

    path('group/<str:unique_id>/edit/', views.edit_group_details, name='edit_group'),
    path('group/<str:unique_id>/delete/', views.delete_group, name='delete_group'),
    
    path('group/<str:unique_id>/posts/', views.group_posts, name='group_posts'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    
    path('<str:unique_id>/create_post/', views.create_post, name='create_post'),
    path('post/<int:post_id>/add_comment/', views.add_comment, name='add_comment'),
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('edit_comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]