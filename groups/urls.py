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

    path('groups/<str:unique_id>/', views.group_dashboard, name='group_dashboard'),
    path('group/<str:unique_id>/requests/', views.group_requests, name='group_requests'),
    path('group/<str:unique_id>/members/', views.group_members, name='group_members'),
    path('group/<str:unique_id>/files/', views.group_files, name='group_files'),

    path('group/<str:unique_id>/accept_request/<int:join_request_id>/', views.accept_request, name='accept_request'),
    path('group/<str:unique_id>/reject_request/<int:join_request_id>/', views.reject_request, name='reject_request'),
    path('group/<str:unique_id>/create_thread/', views.create_discussion_thread, name='create_discussion_thread'),
    # path('thread/<int:thread_id>/add_comment/', views.add_comment, name='add_comment'),
]
