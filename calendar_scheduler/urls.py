from django.urls import path
from . import views

urlpatterns = [
    path('create_event', views.create_event, name='create_event'),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('upcoming_event/', views.upcoming_event_list, name='upcoming_event'),
    path('past_event/', views.past_event_list, name='past_event'),
    path('', views.attended_event_list, name='attended_event'),   
    path('edit/<int:event_id>/', views.edit_event, name='edit_event'),
]