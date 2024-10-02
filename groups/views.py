from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import StudyGroupForm, JoinGroupForm
from .models import StudyGroup

@login_required
def index(request):
    # return render(request, 'index.html')
    # study_groups = StudyGroup.objects.all()  # used if needed 
    
    created_groups = StudyGroup.objects.filter(user=request.user)
    joined_groups = StudyGroup.objects.filter(members=request.user)
    return render(request, 'index.html', {
        'created_groups': created_groups,
        'joined_groups': joined_groups,
    })

@login_required
def create_group(request):
    if request.method == 'POST':
        form = StudyGroupForm(request.POST)
        if form.is_valid():
            study_group = form.save(commit=False) 
            study_group.user = request.user
            study_group.save()
            return redirect('index') 
    else:
        form = StudyGroupForm()
    return render(request, 'create_group.html', {'form': form})

@login_required
def join_group(request):
    if request.method == 'POST':
        form = JoinGroupForm(request.POST)
        if form.is_valid():
            group_code = form.cleaned_data['group_code']
            try:
                study_group = StudyGroup.objects.get(unique_id=group_code)
                
                if request.user not in study_group.members.all():
                    study_group.members.add(request.user)
                    study_group.save()
                    messages.success(request, f'You have successfully joined the group: {study_group.group_name}')
                else:
                    messages.info(request, 'You are already a member of this group.')
                
                return redirect('index') # For now, go back to index/home page
            except StudyGroup.DoesNotExist:
                messages.error(request, 'No group found with that code.')
    else:
        form = JoinGroupForm()

    return render(request, 'join_group.html', {'form': form})