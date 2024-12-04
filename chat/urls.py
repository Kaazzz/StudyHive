from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat, name='chat'),
    path('create_chat', views.create_chat, name='create_chat'),
    path('<int:post_id>/send_message/', views.send_message, name='send_message'),
    path('uploadfile', views.file_upload, name='file_upload'),
    path('download/<int:file_id>/', views.download_file, name='download_file'),
    path('delete/<int:file_id>/', views.delete_file, name='delete_file'),
]

