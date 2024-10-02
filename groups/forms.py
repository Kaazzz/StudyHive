from django import forms
from .models import StudyGroup

class StudyGroupForm(forms.ModelForm):
    class Meta:
        model = StudyGroup
        fields = ['group_name', 'subject', 'description', 'is_private']

class JoinGroupForm(forms.Form):
    group_code = forms.CharField(max_length=6, label="Enter Group Code")

