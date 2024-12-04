from django.shortcuts import render, redirect, get_object_or_404
from .models import Chat_Room, Message, UploadedFile
from .forms import Chat_RoomForm, MessageForm, FileUploadForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.


@login_required
def chat(request):
    chats = Chat_Room.objects.all()
    return render(request, 'chat_room.html', {'chats': chats})  # Use plural 'chats'


@login_required
def create_chat(request):
    """Creates a new chat room if the form is valid."""

    if request.method == 'POST':
        form = Chat_RoomForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  # Prevent initial save
            post.author = request.user
            post.save()
            return redirect('chat')  # Redirect to the chat list view
    else:
        form = Chat_RoomForm()

    return render(request, 'create_chatroom.html', {'form': form})


@login_required
def send_message(request, chat_id):
    """Sends a message to an existing chat room."""
    message = get_object_or_404(Chat_Room, pk=chat_id)
    chat_room = Chat_Room.objects.all()

    if request.method == 'POST':
        form = MessageForm(request.POST or None) 
        if form.is_valid():
            comment = form.save(commit=False)  # Prevent initial save
            comment.chat_room = message
            comment.author = request.user
            comment.save()
            # needs post_id to go back to the chat_room
            return redirect('send_message', chat_id=chat_id)
    else:
        form = MessageForm()

    context = {
        'form': form,
        'chat': message,  # Pass the specific chat room object
        'chat_id': chat_id,  # Include the chat_id for template use
        'chats': chat_room, 
    }

    return render(request, 'send_message.html', context)

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



def download_file(request, file_id):
    file = get_object_or_404(UploadedFile, pk=file_id)
    file_path = file.file.path
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; 1  filename="' + file.file.name + '"'
    return response

def delete_file(request, file_id):
    file = get_object_or_404(UploadedFile, pk=file_id)
    file.delete()
    return redirect('file_upload')
