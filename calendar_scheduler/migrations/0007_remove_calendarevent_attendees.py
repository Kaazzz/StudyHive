# Generated by Django 5.1.3 on 2024-12-09 07:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calendar_scheduler', '0006_calendarevent_attendees'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='calendarevent',
            name='attendees',
        ),
    ]
