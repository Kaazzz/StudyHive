from django import forms
from .models import StudyGroup, DiscussionThread, Comment

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

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['description']