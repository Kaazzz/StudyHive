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
                messages.success(request, "Login successful!")
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
            user = form.save()  
            
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.save()  
            
           
            profile = Profile.objects.get(user=user)
            profile.birthday = form.cleaned_data.get('birthday')
            profile.save()  

            messages.success(request, f'Account created for {user.username}!')
            return redirect('login') 
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
