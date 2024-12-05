from django.urls import path
from . import views

urlpatterns = [
    path('create_event', views.create_event, name='create_event'),
    path('', views.event_list, name='event_list'), 
]