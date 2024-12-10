from django.urls import path
from . import views

urlpatterns = [
    path('create_event', views.create_event, name='create_event'),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('', views.calendar_management, name='calendar_management'), 
    path('edit/<int:event_id>/', views.edit_event, name='edit_event'),
]