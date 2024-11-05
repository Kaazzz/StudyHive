from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import StudyGroupForm, JoinGroupForm
from .models import StudyGroup
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

import json

@login_required
def home(request):
    # return render(request, 'index.html')
    # study_groups = StudyGroup.objects.all()  # used if needed 
    
    created_groups = StudyGroup.objects.filter(user=request.user)
    joined_groups = StudyGroup.objects.filter(members=request.user)
    return render(request, 'home.html', {
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
            return redirect('home') 
    else:
        form = StudyGroupForm()
    return render(request, 'create_group.html', {'form': form})

# @login_required
# def join_group(request):
#     if request.method == 'POST':
#         form = JoinGroupForm(request.POST)
#         if form.is_valid():
#             group_code = form.cleaned_data['group_code']
#             try:
#                 study_group = StudyGroup.objects.get(unique_id=group_code)
                
#                 if request.user not in study_group.members.all():
#                     study_group.members.add(request.user)
#                     study_group.save()
#                     messages.success(request, f'You have successfully joined the group: {study_group.group_name}')
#                 else:
#                     messages.info(request, 'You are already a member of this group.')
                
#                 return redirect('home') # For now, go back to home page
#             except StudyGroup.DoesNotExist:
#                 messages.error(request, 'No group found with that code.')
#     else:
#         form = JoinGroupForm()

#     return render(request, 'join_group.html', {'form': form})

# @login_required
# def join_group(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)  # Get the request body
#         group_code = data.get('group_code')
#         try:
#             study_group = StudyGroup.objects.get(unique_id=group_code)

#             if request.user not in study_group.members.all():
#                 study_group.members.add(request.user)
#                 study_group.save()
#                 return JsonResponse({
#                     'message': 'Successfully joined the group!',  # Include a success message
#                     'redirect_url': f'/groups/{study_group.unique_id}/'
#                 }, status=200)
#             else:
#                 return JsonResponse({'message': 'You are already a member of this group.'}, status=400)

#         except StudyGroup.DoesNotExist:
#             return JsonResponse({'message': 'No group found with that code.'}, status=404)

#     return JsonResponse({'message': 'Invalid request method.'}, status=400)

# @login_required
# def join_group(request):
#     if request.method == 'POST':
#         form = JoinGroupForm(request.POST)
#         if form.is_valid():
#             group_code = form.cleaned_data['group_code']
#             try:
#                 study_group = StudyGroup.objects.get(unique_id=group_code)
                
#                 if request.user not in study_group.members.all():
#                     study_group.members.add(request.user)
#                     study_group.save()
#                     messages.success(request, f'You have successfully joined the group: {study_group.group_name}')
#                 else:
#                     messages.info(request, 'You are already a member of this group.')
                
#                 return redirect('home') # For now, go back to home page
#             except StudyGroup.DoesNotExist:
#                 messages.error(request, 'No group found with that code.')
#     else:
#         form = JoinGroupForm()

#     return render(request, 'join_group.html', {'form': form})

@login_required
def join_group(request):
    if request.method == 'POST':
        # Check if the request is an AJAX request
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Handle AJAX request
            data = json.loads(request.body)  # Get the request body
            group_code = data.get('group_code')
            try:
                study_group = StudyGroup.objects.get(unique_id=group_code)

                if request.user not in study_group.members.all():
                    study_group.members.add(request.user)
                    study_group.save()
                    return JsonResponse({
                        'message': 'Successfully joined the group!',
                        'redirect_url': f'/groups/{study_group.unique_id}/'
                    }, status=200)
                else:
                    return JsonResponse({'message': 'You are already a member of this group.'}, status=400)

            except StudyGroup.DoesNotExist:
                return JsonResponse({'message': 'No group found with that code.'}, status=404)

        else:
            # Handle traditional POST request
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

                    return redirect('home')  # Redirect to home page after joining
                except StudyGroup.DoesNotExist:
                    messages.error(request, 'No group found with that code.')
            else:
                form = JoinGroupForm()  # If the form is invalid, create a new instance

    else:
        form = JoinGroupForm()  # Handle GET requests by creating a new form instance

    return render(request, 'join_group.html', {'form': form})

@login_required
def group_dashboard(request, unique_id):
    group = get_object_or_404(StudyGroup, unique_id=unique_id)

    if request.method == 'POST':
        # Handle the request to join the group
        if request.user not in group.members.all():
            group.members.add(request.user)
            messages.success(request, f'You have successfully joined the group: {group.group_name}')
        else:
            messages.info(request, 'You are already a member of this group.')
        
        # After joining, redirect back to the same group dashboard
        return redirect('group_dashboard', unique_id=unique_id)

    # If it's a GET request, just render the dashboard
    return render(request, 'group_dashboard.html', {'group': group})



# @require_GET
# def search_groups(request):
#     query = request.GET.get('query', '').strip()
#     filter_option = request.GET.get('filter', 'all')
    
#     results = StudyGroup.objects.none() 

#     if query:
#         if filter_option == 'group':
#             results = StudyGroup.objects.filter(group_name__icontains=query)
#         elif filter_option == 'member':
#             results = StudyGroup.objects.filter(members__username__icontains=query)
#         elif filter_option == 'subject':
#             results = StudyGroup.objects.filter(subject__icontains=query)
#         elif filter_option == 'all':
#             results = StudyGroup.objects.filter(
#                 Q(group_name__icontains=query) |
#                 Q(subject__icontains=query) |
#                 Q(members__username__icontains=query)
#             )
    
#     response_data = {
#         'results': [{'group_name': group.group_name, 'subject': group.subject, 'members_count': group.members.count(), 'unique_id': group.unique_id} for group in results]
#     }
    
#     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         return JsonResponse(response_data)
#     else:
#         return render(request, 'home.html', {'query': query, 'results': response_data['results']})
@login_required
def search_groups(request):
    query = request.GET.get('query', '').strip()
    filter_option = request.GET.get('filter', 'all')
    
    results = StudyGroup.objects.none()  # Start with no results

    # Search according to the selected filter
    if query:
        if filter_option == 'group':
            results = StudyGroup.objects.filter(group_name__icontains=query)
        elif filter_option == 'member':
            results = StudyGroup.objects.filter(members__username__icontains=query)
        elif filter_option == 'subject':
            results = StudyGroup.objects.filter(subject__icontains=query)
        elif filter_option == 'all':
            results = StudyGroup.objects.filter(
                Q(group_name__icontains=query) |
                Q(subject__icontains=query) |
                Q(members__username__icontains=query)
            ).distinct()
    
    # Prepare response data
    user = request.user
    response_data = {
        'results': [
            {
                'group_name': group.group_name,
                'subject': group.subject,
                'members_count': group.members.count(),
                'unique_id': group.unique_id,
                'is_member': group.members.filter(id=user.id).exists(),
                'is_creator': group.user == user,
                'is_private': getattr(group, 'is_private', False),  # Assuming `is_private` exists
            }
            for group in results
        ]
    }
    
    # Send JSON response for AJAX requests; render `home.html` otherwise
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse(response_data)
    else:
        return render(request, 'home.html', {'query': query, 'results': response_data['results']})