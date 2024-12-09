from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class CalendarEvent(models.Model):
    title = models.CharField(max_length=50)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.TextField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError(('End time must be after start time.'))