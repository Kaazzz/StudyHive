from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm

class CustomUserCreationForm(UserCreationForm):
    birthday = forms.DateField(widget=forms.DateInput(attrs={
        'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50',
        'type': 'date'
    }), required=False)
    
    # Adding first name and last name fields
    first_name = forms.CharField(max_length=30, required=True, 
                                  widget=forms.TextInput(attrs={
                                      'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50',
                                      'placeholder': ''
                                  }))
    last_name = forms.CharField(max_length=30, required=True, 
                                 widget=forms.TextInput(attrs={
                                     'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50',
                                     'placeholder': ''
                                 }))
    
    birthday = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50',
            'type': 'date'
        }), 
        required=False
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'birthday')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50'
            })


class CustomLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50',
        'placeholder': 'Password'
    }))


from django import forms
from django.contrib.auth.models import User

class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True,
                                  widget=forms.TextInput(attrs={
                                      'class': 'mt-4 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 px-4 py-3',  # Added padding
                                  }))
    last_name = forms.CharField(max_length=30, required=True,
                                 widget=forms.TextInput(attrs={
                                     'class': 'mt-4 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 px-4 py-3',  # Added padding
                                 }))
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={
                                 'class': 'mt-4 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 px-4 py-3',  # Added padding
                             }))
    birthday = forms.DateField(required=False,
                                widget=forms.DateInput(attrs={
                                    'class': 'mt-4 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 px-4 py-3',  # Added padding
                                    'type': 'date',
                                }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'birthday']




from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'mt-5 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 px-4 py-3',
        'placeholder': 'Current Password'
    }))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'mt-5 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 px-4 py-3',
        'placeholder': 'New Password'
    }))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'mt-5 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 px-4 py-3',
        'placeholder': 'Confirm New Password'
    }))

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

