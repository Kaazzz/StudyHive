from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import StudyGroupForm, JoinGroupForm, DiscussionThreadForm, StudyGroupEditForm
# from .forms import CommentForm
from .models import StudyGroup, JoinRequest, DiscussionThread
from django.db.models import Q, Count
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

import json

# previous version
@login_required
def group_dashboard(request, unique_id):
    group = get_object_or_404(StudyGroup, unique_id=unique_id)

    threads = DiscussionThread.objects.filter(group_id=group)

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
    return render(request, 'group_dashboard.html', {'group': group, 'threads': threads})

def edit_group_details(request, unique_id):
    group = get_object_or_404(StudyGroup, unique_id=unique_id)  # Get the group by unique_id
    
    if request.method == 'POST':
        form = StudyGroupEditForm(request.POST, instance=group)
        if form.is_valid():
            form.save()  # Save changes to the database
            messages.success(request, 'Group details updated successfully!')
            return redirect('group_dashboard', unique_id=group.unique_id)  # Redirect back to the dashboard
    else:
        form = StudyGroupEditForm(instance=group)  # Pre-fill the form with existing group data

    return render(request, 'edit_group.html', {'form': form, 'group': group})

def delete_group(request, unique_id):
    group = get_object_or_404(StudyGroup, unique_id=unique_id)

    if request.method == "POST":
        group_name = group.group_name
        group.delete()
        messages.success(request, f'Group "{group_name}" has been deleted successfully!')
        return redirect('home')

    return render(request, 'confirm_delete_group.html', {'group': group})

def create_discussion_thread(request, unique_id):
    group = get_object_or_404(StudyGroup, unique_id=unique_id)  # Get group using unique_id
    if request.method == "POST":
        form = DiscussionThreadForm(request.POST)
        if form.is_valid():
            discussion_thread = form.save(commit=False)
            discussion_thread.group_id = group
            discussion_thread.save()
            # Redirect to the group's dashboard using unique_id
            return redirect('group_dashboard', unique_id=unique_id)
    else:
        form = DiscussionThreadForm()
    return render(request, 'create_thread.html', {'form': form, 'group': group})

# @login_required
# def add_comment(request, thread_id):
#     thread = get_object_or_404(DiscussionThreadForm, id=thread_id)
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.user_id = request.user
#             comment.discussion_id = thread
#             comment.save()
#             return redirect('group_dashboard', group_id=thread.group_id.id)
#     else:
#         form = CommentForm()
#     return render(request, 'add_comment.html', {'form': form, 'thread': thread})

@login_required
def profile_view(request):
    return render(request, 'groups/profile.html', {'user': request.user})

@login_required
def home_page(request):
    return render(request, 'home_page.html', {'user': request.user})

# JoinRequest Private
@login_required
def accept_request(request, unique_id, join_request_id):
    if request.method == 'POST':
        try:
            # Fetch the group using the unique_id
            study_group = StudyGroup.objects.get(unique_id=unique_id)

            # Fetch the join request using join_request_id
            join_request = JoinRequest.objects.get(join_request_id=join_request_id, group=study_group)

            # Add the user who made the join request to the group's members
            study_group.members.add(join_request.user)
            study_group.save()

            # Update join request status and set processed_by
            join_request.status = 'accepted'
            join_request.processed_by = request.user
            join_request.processed_at = datetime.now()
            join_request.save()

            # Prepare response data
            response_data = {
                'message': f'{join_request.user.username}: accepted by {request.user.username}',
                'join_request_id': join_request_id
            }

            # return render(request, 'group_requests.html')
            return JsonResponse(response_data, status=200)

        except StudyGroup.DoesNotExist:
            return JsonResponse({'message': 'Group not found.'}, status=404)
        except JoinRequest.DoesNotExist:
            return JsonResponse({'message': 'Join request not found.'}, status=404)

    return JsonResponse({'message': 'Invalid request.'}, status=400)

@login_required
def reject_request(request, unique_id, join_request_id):
    if request.method == 'POST':
        try:
            # Fetch the group using the unique_id
            study_group = StudyGroup.objects.get(unique_id=unique_id)

            # Fetch the join request using join_request_id
            join_request = JoinRequest.objects.get(join_request_id=join_request_id, group=study_group)

            # Update join request status to rejected and set processed_by
            join_request.status = 'rejected'
            join_request.processed_by = request.user
            join_request.processed_at = datetime.now()
            join_request.save()

            # Prepare response data
            response_data = {
                'message': f'{join_request.user.username}: rejected by {request.user.username}',
                'join_request_id': join_request_id
            }
            return JsonResponse(response_data, status=200)

        except StudyGroup.DoesNotExist:
            return JsonResponse({'message': 'Group not found.'}, status=404)
        except JoinRequest.DoesNotExist:
            return JsonResponse({'message': 'Join request not found.'}, status=404)

    return JsonResponse({'message': 'Invalid request.'}, status=400)

@login_required
def group_requests(request, unique_id):
    group = get_object_or_404(StudyGroup, unique_id=unique_id)

    # Fetch pending and processed requests
    pending_requests = JoinRequest.objects.filter(group=group, status='pending')
    processed_requests = JoinRequest.objects.filter(group=group).exclude(status='pending')

    context = {
        'group': group,
        'pending_requests': pending_requests,
        'processed_requests': processed_requests,
    }
    return render(request, 'group_requests.html', context)

@login_required
def group_members(request, unique_id):
    group = get_object_or_404(StudyGroup, unique_id=unique_id)

    context = {
        'group': group,
    }

    # Add any necessary logic for displaying group members here
    return render(request, 'group_members.html', context)

@login_required
def remove_member(request, unique_id, member_id):
    group = get_object_or_404(StudyGroup, unique_id=unique_id)
    
    if request.user != group.user:  # Ensure only the creator can remove members
        messages.error(request, "You don't have permission to remove members.")
        return redirect('group_members', unique_id=unique_id)

    member = get_object_or_404(User, id=member_id)
    if member == group.user:
        messages.error(request, "You cannot remove the group creator.")
        return redirect('group_members', unique_id=unique_id)

    group.members.remove(member)
    messages.success(request, f"{member.first_name} {member.last_name} has been removed.")
    return redirect('group_members', unique_id=unique_id)

@login_required
def group_files(request, unique_id):
    group = get_object_or_404(StudyGroup, unique_id=unique_id)

    context = {
        'group': group,
    }

    # Add any necessary logic for managing group files here
    return render(request, 'group_files.html', context)

def request_join(request):
    if request.method == 'POST':
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)

            # Get the group ID from the request
            group_id = data.get('group_id')
            if not group_id:
                return JsonResponse({'message': 'Group ID is required'}, status=400)

            # Get the group object, or return 404 if not found
            group = get_object_or_404(StudyGroup, unique_id=group_id)

            # Get the user (the one making the request)
            user = request.user

            # Check if the user is already a member of the group
            if user in group.members.all():
                return JsonResponse({'message': 'You are already a member of this group.'}, status=400)

            # Check if the user has already requested to join this group
            existing_request = JoinRequest.objects.filter(user=user, group=group, status='pending').first()
            if existing_request:
                return JsonResponse({'message': 'You have already sent a join request.'}, status=400)

            # Create a new join request
            join_request = JoinRequest.objects.create(user=user, group=group, status='pending')

            return JsonResponse({'message': 'Your request to join the group has been sent successfully.'})
        
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)

    return JsonResponse({'message': 'Invalid request method'}, status=405)

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

# @login_required
# def search_groups(request):
#     query = request.GET.get('query', '').strip()
#     filter_option = request.GET.get('filter', 'all')

#     results = StudyGroup.objects.none()  # Start with no results

#     # Search according to the selected filter
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
#             ).distinct()

#     # Annotate results with the member count
#     results = results.annotate(members_count=Count('members'))

#     context = {
#         'results': results,  # Pass results to the template
#     }

#     return render(request, 'search_groups.html', context)

@login_required
def search_groups(request):
    query = request.GET.get('query', '').strip()
    filter_option = request.GET.get('filter', 'all')

    results = StudyGroup.objects.none()  # Start with no results

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
    else:  # If there's no query, return all groups for 'all' filter
        if filter_option == 'all':
            results = StudyGroup.objects.all()  # Get all groups

    results = results.annotate(members_count=Count('members'))

    groups_data = []
    for group in results:
        # Check if the user is the owner
        is_owner = group.user == request.user

        # Check if the user is a member
        is_member = request.user in group.members.all()

        # Debugging output to ensure correctness
        print(f"Group: {group.group_name}, Is Owner: {is_owner}, Is Member: {is_member}")

        groups_data.append({
            'group': group,
            'is_owner': is_owner,
            'is_member': is_member,
        })

    context = {
        'groups_data': groups_data,
        'user': request.user,
        'results': results,
    }

    return render(request, 'search_groups.html', context)


