from django.contrib import admin
from .models import Chat_Room, Message, UploadedFile

admin.site.register(Chat_Room)
admin.site.register(Message)
admin.site.register(UploadedFile)