from django.contrib import admin
from .models import StudyGroup, JoinRequest, GroupFiles

class StudyGroupAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'subject', 'created_at', 'is_private')  # Customize fields to display
    search_fields = ('group_name', 'subject')  # Enable search functionality
    list_filter = ('is_private',)  # Add filters for private groups

admin.site.register(StudyGroup)
admin.site.register(JoinRequest)
admin.site.register(GroupFiles)
