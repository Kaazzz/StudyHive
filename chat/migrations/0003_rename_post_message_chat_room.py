# Generated by Django 5.1.1 on 2024-12-03 12:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_remove_message_name_message_author'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='post',
            new_name='chat_room',
        ),
    ]
