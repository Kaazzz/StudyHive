from django.db import models
from django.contrib.auth.models import User
import random
import string

class StudyGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='created_groups') # accept sag null kay daghan arte
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
