from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomLoginForm
from .models import Profile
def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Adjust this to your home URL name
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = CustomLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user first
            
            # Save first name and last name after user creation
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.save()  # Save the user's first and last name
            
            # Get the cleaned birthday value from the form
            birthday = form.cleaned_data.get('birthday')
            
            # Create the profile if it doesn't already exist
            profile, created = Profile.objects.get_or_create(user=user)
            
            # Set the birthday for the profile
            profile.birthday = birthday
            profile.save()  # Save the profile

            # Provide success feedback
            messages.success(request, f'Account created for {user.username}!')
            return redirect('login')  # Redirect to login after successful registration
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('login')  

def landing_page_view(request):
    return render(request, 'accounts/index.html')  # Replace with your landing page template


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import EditProfileForm

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your personal information has been updated.')
            return redirect('profile')  # Redirect to profile page (or change this URL name)
    else:
        form = EditProfileForm(instance=request.user)
    
    return render(request, 'accounts/edit_profile.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import CustomPasswordChangeForm  # Import your custom form

def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Keep the user logged in after password change
            messages.success(request, 'Your password has been updated successfully!')
            return redirect('profile')  # Or wherever you want to redirect after success
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(user=request.user)

    return render(request, 'accounts/change_password.html', {'form': form})
