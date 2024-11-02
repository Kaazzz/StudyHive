from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('create/', views.create_group, name='create_group'),
    path('join/', views.join_group, name='join_group'),
    path('groups/<str:unique_id>/', views.group_dashboard, name='group_dashboard'),
]
