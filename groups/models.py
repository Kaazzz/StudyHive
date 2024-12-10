from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

import random
import string

class StudyGroup(models.Model):
    group_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='created_groups') # creator
    group_name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100, default="General")  # Default subject
    description = models.TextField()
    is_private = models.BooleanField(default=False)
    unique_id = models.CharField(max_length=6, unique=True, blank=True)  # Unique ID for joining
    members = models.ManyToManyField(User, related_name='study_groups', blank=True)  # Members can join the group

    def save(self, *args, **kwargs):
        # Generate a unique 6-letter ID for the group if not provided
        if not self.unique_id:
            self.unique_id = self.generate_unique_id()
        super().save(*args, **kwargs)

    def generate_unique_id(self):
        # Generate a unique 6-letter ID
        while True:
            unique_id = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
            if not StudyGroup.objects.filter(unique_id=unique_id).exists():  # Ensure it's unique
                return unique_id

    def __str__(self):
        return self.group_name
    
    def get_dashboard_url(self):
        return reverse('group_dashboard', args=[self.unique_id])

    def get_members_url(self):
        return reverse('group_members', args=[self.unique_id])

    def get_requests_url(self):
        return reverse('group_requests', args=[self.unique_id])

    def get_files_url(self):
        return reverse('group_files', args=[self.unique_id])
    
    class Profile(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE)
        birthday = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class JoinRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    join_request_id = models.AutoField(primary_key=True)  # Auto-incrementing ID for the request
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='join_requests')  # The user requesting to join
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, related_name='join_requests')  # The group being joined
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')  # Status of the request
    processed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='processed_requests')  # Admin who processed the request
    processed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Request {self.join_request_id} - {self.user.username} to {self.group.group_name}"
    
class DiscussionThread(models.Model):
    discussion_id = models.AutoField(primary_key=True)
    group_id = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, related_name='discussion_thread')
    session_date = models.DateTimeField(null=True, blank=True)
    topic = models.CharField(max_length=100, default="General")
    description = models.TextField(null=True)

# class Comment(models.Model):
#     comment_id = models.AutoField(primary_key=True)
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment')
#     discussion_id = models.ForeignKey(DiscussionThread, on_delete=models.CASCADE, related_name='comment')
#     topic = models.CharField(max_length=100, default="General")
#     description = models.TextField(null=True)
#     timestamp = models.DateTimeField(null=True)


