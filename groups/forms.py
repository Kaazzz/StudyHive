from django import forms
from .models import StudyGroup, DiscussionThread, GroupFiles
from posts.models import Post, Comment

class StudyGroupForm(forms.ModelForm):
    class Meta:
        model = StudyGroup
        fields = ['group_name', 'subject', 'description', 'is_private']

class JoinGroupForm(forms.Form):
    group_code = forms.CharField(max_length=6, label="Enter Group Code")

class DiscussionThreadForm(forms.ModelForm):
    session_date = forms.DateTimeField(
        widget=forms.TextInput(attrs={'type': 'datetime-local'}),
        required=False,
        label="Session Date"
    )

    class Meta:
        model = DiscussionThread
        fields = ['topic', 'description', 'session_date']

class StudyGroupEditForm(forms.ModelForm):
    class Meta:
        model = StudyGroup
        fields = ['group_name', 'subject', 'description', 'is_private']  # Fields to include in the form
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
        }

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = GroupFiles
        fields = ['file']