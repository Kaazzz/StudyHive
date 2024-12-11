from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import StudyGroupForm, JoinGroupForm, DiscussionThreadForm, StudyGroupEditForm, UploadFileForm
from .models import StudyGroup, JoinRequest, DiscussionThread, GroupFiles
from posts.models import Post, Comment
from django.db.models import Q, Count, Case, When, Value, IntegerField
from django.http import JsonResponse, Http404
from django.shortcuts import render
from django.views.decorators.http import require_GET

import json

@login_required
def group_posts(request, unique_id):
    # Get the group by unique_id
    group = get_object_or_404(StudyGroup, unique_id=unique_id)
    
    # Fetch all posts related to this group
    posts = Post.objects.filter(group=group).order_by('-created_at')

    # Handle creating a new post
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        if title and description:
            new_post = Post(title=title, description=description, author=request.user, group=group)
            new_post.save()
            return redirect('group_posts', unique_id=unique_id)

    # Render the group posts page with the group and its posts
    return render(request, 'group_posts.html', {'group': group, 'posts': posts})

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    group = post.group  # Get the group for the post

    # Get all comments for this post
    comments = Comment.objects.filter(post=post).order_by('-created_at')

    # Add a new comment
    if request.method == 'POST' and 'comment_text' in request.POST:
        text = request.POST.get('comment_text')
        if text:
            new_comment = Comment(text=text, author=request.user, post=post, group=group)
            new_comment.save()
            return redirect('post_detail', post_id=post.id)

    # Edit a comment (if the user is the author)
    if request.method == 'POST' and 'edit_comment_id' in request.POST:
        comment_id = request.POST.get('edit_comment_id')
        new_text = request.POST.get('edit_comment_text')
        if new_text:
            comment = get_object_or_404(Comment, id=comment_id, author=request.user)
            comment.text = new_text
            comment.save()
            return redirect('post_detail', post_id=post.id)

    # Delete a comment (if the user is the author)
    if request.method == 'POST' and 'delete_comment_id' in request.POST:
        comment_id = request.POST.get('delete_comment_id')
        comment = get_object_or_404(Comment, id=comment_id, author=request.user)
        comment.delete()
        return redirect('post_detail', post_id=post.id)

    return render(request, 'post_detail.html', {'post': post, 'group': group, 'comments': comments})

# Post
@login_required
def create_post(request, unique_id):
    group = get_object_or_404(StudyGroup, unique_id=unique_id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        if title and description:
            Post.objects.create(
                title=title,
                description=description,
                author=request.user,
                group_id=group
            )
            messages.success(request, "Post created successfully!")
            return redirect('group_dashboard', unique_id=unique_id)
        else:
            messages.error(request, "Title and description are required.")
    
    return render(request, 'groups/create_post.html', {'group': group})


# To be checked
@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            comment = Comment.objects.create(
                post=post,
                text=text,
                author=request.user,
                group=post.group  # Assign the same group as the post
            )
            # Return the comment data as JSON
            return JsonResponse({
                'success': True,
                'comment': {
                    'id': comment.id,
                    'text': comment.text,
                    'author': comment.author.username,
                    'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
                }
            })
        return JsonResponse({'success': False, 'error': 'Comment text is required.'}, status=400)

    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)

# Edit
def edit_comment(request, comment_id):
    if request.method == "POST":
        comment = get_object_or_404(Comment, id=comment_id)

        # Ensure the user is the comment author
        if comment.author == request.user:
            new_text = request.POST.get('text', '').strip()
            if new_text:
                comment.text = new_text
                comment.save()
                return JsonResponse({"success": True, "comment": {"text": comment.text}})
            else:
                return JsonResponse({"success": False, "error": "Comment cannot be empty."})
        return JsonResponse({"success": False, "error": "You are not the author of this comment."})
    return JsonResponse({"success": False, "error": "Invalid request method."})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        if title and description:
            post.title = title
            post.description = description
            post.save()
            messages.success(request, "Post updated successfully!")
        else:
            messages.error(request, "Title and description cannot be empty.")
        return redirect('group_dashboard', unique_id=post.group_id.unique_id)
    
    return render(request, 'groups/edit_post.html', {'post': post})

# Delete
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Ensure that the user is the author of the comment or an admin
    if comment.author == request.user or request.user.is_staff:
        comment.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'error': 'You are not authorized to delete this comment.'}, status=403)

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    unique_id = post.group_id.unique_id
    post.delete()
    messages.success(request, "Post deleted successfully!")
    return redirect('group_dashboard', unique_id=unique_id)


def group_files_view(request, group_id):
    # Retrieve the group using unique_id, as you're passing that in the URL
    group = get_object_or_404(StudyGroup, unique_id=group_id)
    
    files = GroupFiles.objects.filter(group_id=group)

    if request.method == 'POST' and request.FILES:
        # Handle file upload
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_instance = form.save(commit=False)
            file_instance.group_id = group
            file_instance.user_id = request.user
            file_instance.save()
            # Redirect using the unique_id, not the id
            return redirect('group_files', group_id=group.unique_id)
    else:
        form = UploadFileForm()

    context = {
        'group': group,
        'files': files,
        'form': form,
    }
    return render(request, 'group_files.html', context)

def delete_file(request, group_id, file_id):
    # Get the group object
    group = get_object_or_404(StudyGroup, unique_id=group_id)
    # Get the file object
    file = get_object_or_404(GroupFiles, id=file_id, group_id=group)

    if request.method == 'DELETE':
        file.delete()
        return JsonResponse({'status': 'success'}, status=200)
    return JsonResponse({'status': 'error'}, status=400)

# previous version
def group_dashboard(request, unique_id):
    # Get the group object or return a 404 if not found
    group = get_object_or_404(StudyGroup, unique_id=unique_id)

    # Retrieve all posts for the group (using filter to allow multiple posts)
    posts = Post.objects.filter(group=group)

    if request.method == 'POST':
        # Handle the request to join the group
        if request.user not in group.members.all():
            group.members.add(request.user)
            messages.success(request, f'You have successfully joined the group: {group.group_name}')
        else:
            messages.info(request, 'You are already a member of this group.')
        
        # After joining, redirect back to the same group dashboard
        return redirect('group_dashboard', unique_id=unique_id)

    # If it's a GET request, just render the dashboard with posts
    return render(request, 'group_dashboard.html', {'group': group, 'posts': posts})

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

@login_required
def profile_view(request):
    return render(request, 'groups/profile.html', {'user': request.user})

@login_required
def home_page(request):
    return render(request, 'home_page.html', {'user': request.user})

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

# # JoinRequest Private
# @login_required
# def accept_request(request, unique_id, join_request_id):
#     if request.method == 'POST':
#         try:
#             # Fetch the group using the unique_id
#             study_group = StudyGroup.objects.get(unique_id=unique_id)

#             # Fetch the join request using join_request_id
#             join_request = JoinRequest.objects.get(join_request_id=join_request_id, group=study_group)

#             # Add the user who made the join request to the group's members
#             study_group.members.add(join_request.user)
#             study_group.save()

#             # Update join request status and set processed_by
#             join_request.status = 'accepted'
#             join_request.processed_by = request.user
#             join_request.processed_at = datetime.now()
#             join_request.save()

#             # Prepare response data
#             response_data = {
#                 'message': f'{join_request.user.username}: accepted by {request.user.username}',
#                 'join_request_id': join_request_id
#             }

#             # return render(request, 'group_requests.html')
#             return JsonResponse(response_data, status=200)

#         except StudyGroup.DoesNotExist:
#             return JsonResponse({'message': 'Group not found.'}, status=404)
#         except JoinRequest.DoesNotExist:
#             return JsonResponse({'message': 'Join request not found.'}, status=404)

#     return JsonResponse({'message': 'Invalid request.'}, status=400)

# @login_required
# def reject_request(request, unique_id, join_request_id):
#     if request.method == 'POST':
#         try:
#             # Fetch the group using the unique_id
#             study_group = StudyGroup.objects.get(unique_id=unique_id)

#             # Fetch the join request using join_request_id
#             join_request = JoinRequest.objects.get(join_request_id=join_request_id, group=study_group)

#             # Update join request status to rejected and set processed_by
#             join_request.status = 'rejected'
#             join_request.processed_by = request.user
#             join_request.processed_at = datetime.now()
#             join_request.save()

#             # Prepare response data
#             response_data = {
#                 'message': f'{join_request.user.username}: rejected by {request.user.username}',
#                 'join_request_id': join_request_id
#             }
#             return JsonResponse(response_data, status=200)

#         except StudyGroup.DoesNotExist:
#             return JsonResponse({'message': 'Group not found.'}, status=404)
#         except JoinRequest.DoesNotExist:
#             return JsonResponse({'message': 'Join request not found.'}, status=404)

#     return JsonResponse({'message': 'Invalid request.'}, status=400)

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
    # Fetch the group by its unique_id
    group = get_object_or_404(StudyGroup, unique_id=unique_id)

    # Fetch all members of the group
    members = group.members.all()

    # Order members such that the creator (group.user) is always first
    sorted_members = members.order_by(
        Case(
            When(id=group.user.id, then=Value(0)),
            default=Value(1),
            output_field=IntegerField()
        )
    )

    # Add the sorted members to the context
    context = {
        'group': group,
        'sorted_members': sorted_members,
    }

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

# @login_required
# def group_files(request, unique_id):
#     group = get_object_or_404(StudyGroup, unique_id=unique_id)

#     context = {
#         'group': group,
#     }

#     # Add any necessary logic for managing group files here
#     return render(request, 'group_files.html', context)

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
    joined_groups = StudyGroup.objects.filter(members=request.user).exclude(user=request.user)
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

            study_group.members.add(request.user)

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


