# Generated by Django 5.1.3 on 2024-12-09 07:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendar_scheduler', '0005_remove_calendarevent_attendees'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='calendarevent',
            name='attendees',
            field=models.ManyToManyField(blank=True, related_name='attended_events', to=settings.AUTH_USER_MODEL),
        ),
    ]
