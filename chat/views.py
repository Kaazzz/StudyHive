from django.shortcuts import render, redirect, get_object_or_404
from .models import Chat_Room, Message, UploadedFile
from .forms import Chat_RoomForm, MessageForm, FileUploadForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User 
# Create your views here.


@login_required
def chat(request):
    chats = Chat_Room.objects.all()
    return render(request, 'chat_room.html', {'chats': chats})  # Use plural 'chats'


@login_required
def create_chat(request):
    if request.method == 'POST':
        form = Chat_RoomForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  # Prevent initial save
            post.author = request.user
            post.save()  # Save the chat room instance first

            # Get selected members from the form
            selected_members = request.POST.getlist('members')

            for username in selected_members:
                user = User.objects.get(username=username)
                post.members.add(user)

            return redirect('chat')
    else:
        form = Chat_RoomForm()

    # Add members selection field to the template context
    context = {'form': form, 'users': User.objects.all().exclude(username=request.user)}  # Exclude current user
    return render(request, 'create_chatroom.html', context)


@login_required
def send_message(request, chat_id):
    chatroom = get_object_or_404(Chat_Room, pk=chat_id)
    chat_room = Chat_Room.objects.all()
    now = timezone.now() - timedelta(minutes=5) 

    if request.method == 'POST':
        form = MessageForm(request.POST or None) 
        if form.is_valid():
            comment = form.save(commit=False)  # Prevent initial save
            comment.chat_room = chatroom
            comment.is_sent = True
            comment.is_reply = False
            comment.author = request.user
            comment.save()
            # needs post_id to go back to the chat_room
            return redirect('send_message', chat_id=chat_id)
    else:
        form = MessageForm()

    context = {
        'form': form,
        'chat': chatroom,  # Pass the specific chat room object
        'chat_id': chat_id,  # Include the chat_id for template use
        'chats': chat_room, 
        'now':now,
    }

    return render(request, 'send_message.html', context)


@login_required
def file_upload(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('file_upload')# Redirect to the same view
    else:
        form = FileUploadForm()

    # Fetch all uploaded files
    files = UploadedFile.objects.all()

    return render(request, 'file_upload.html', {'form': form, 'files': files})


@login_required
def download_file(request, file_id):
    file = get_object_or_404(UploadedFile, pk=file_id)
    file_path = file.file.path
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; 1  filename="' + file.file.name + '"'
    return response

@login_required
def delete_file(request, file_id):
    file = get_object_or_404(UploadedFile, pk=file_id)
    file.delete()
    return redirect('file_upload')

@login_required
def edit_chat(request, chat_id):
    chat_room = get_object_or_404(Chat_Room, pk=chat_id)

    # Check if the user is authorized to edit the post
    if request.user != chat_room.author:
        return HttpResponse("You are not authorized to edit this post.")

    if request.method == 'POST':
        # Update the existing post instance with form data
        form = Chat_RoomForm(request.POST, instance=chat_room)
        if form.is_valid():
            selected_users = request.POST.getlist('members')
            for user_id in selected_users:
                user = User.objects.get(pk=user_id)  # Get user object based on ID
                chat_room.members.add(user)
            form.save()
            return redirect('send_message', chat_id=chat_id)
    else:
        # Pre-populate the form with existing post data
        form = Chat_RoomForm(instance=chat_room)
        users = chat_room.members.all() 

    return render(request, 'edit_chat_room.html', {'form': form, 'chat': chat_room, 'users': users})

@login_required
def edit_message(request, message_id, chat_id):
    chat_rooms = Chat_Room.objects.all()
    message = get_object_or_404(Message, pk=message_id)

    # Check if the user is authorized to edit the comment (e.g., only the author)
    if request.user != message.author:
        return HttpResponse("You are not authorized to edit this comment.")

    if request.method == 'POST':
        # Update the existing comment instance with form data
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect('send_message', chat_id)  
            
    else:
        # Pre-populate the form with existing comment data
        form = MessageForm(instance=message)

    return render(request, 'edit_message.html', {'form': form, 'message': message, 'chats':chat_rooms})


@login_required
def reply_message(request, chat_id, message_id):
    chatroom = get_object_or_404(Chat_Room, pk=chat_id)
    chat_rooms = Chat_Room.objects.all()
    reply = get_object_or_404(Message, pk=message_id)

    if request.method == 'POST':
        form = MessageForm(request.POST or None) 
        if form.is_valid():
            comment = form.save(commit=False)  # Prevent initial save
            comment.chat_room = chatroom
            comment.is_sent = True
            comment.reply = reply.text
            comment.is_reply = True
            comment.author = request.user
            comment.save()
            # needs post_id to go back to the chat_room
            return redirect('send_message', chat_id=chat_id)
    else:
        form = MessageForm()

    context = {
        'form': form,
        'chat': chatroom,  # Pass the specific chat room object
        'chat_id': chat_id,  # Include the chat_id for template use
        'chats': chat_rooms, 
        'reply':reply,
    }

    return render(request, 'reply_message.html', context)

@login_required
def delete_message(request, message_id, chat_id):
    message = Message.objects.get(id=message_id)
    message.is_sent = False
    message.save()
    return redirect('send_message', chat_id=chat_id) 
