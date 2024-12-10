from django import forms
from .models import Chat_Room, Message, UploadedFile

class Chat_RoomForm(forms.ModelForm):
    class Meta:
        model = Chat_Room
        fields = ['title', 'description']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields =('text',)

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs = {'rows': 3}

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ('file',)
