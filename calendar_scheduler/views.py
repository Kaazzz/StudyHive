from django.shortcuts import render,redirect, get_object_or_404
from .forms import CalendarEventForm, CalendarEvent
from django.contrib.auth.decorators import login_required
from django.utils import timezone

@login_required
def create_event(request):
    if request.method == 'POST':
        form = CalendarEventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.author = request.user
            event.save()
            # Handle successful form submission, e.g., redirect
            return redirect('attended_event')
    else:
        form = CalendarEventForm()

    return render(request, 'create_event.html', {'form': form})

@login_required
def event_list(request):
    events = CalendarEvent.objects.all()
    today = timezone.now()  # Format the date as needed
    now = timezone.now()
    return render(request, 'event_list.html', {'events': events,'user': request.user,'today': today} )


@login_required
def delete_event(request, event_id):
    event = get_object_or_404(CalendarEvent, pk=event_id)
    event.delete()
    return redirect('calendar_management') 


@login_required
def upcoming_event_list(request):
    events = CalendarEvent.objects.all()
    today = timezone.now()  # Format the date as needed
    now = timezone.now()
    return render(request, 'upcoming_event_list.html', {'events': events,'user': request.user,'today': today} )

@login_required
def calendar_management(request):
    events = CalendarEvent.objects.all()
    today = timezone.now()  # Format the date as needed
    now = timezone.now()

    if request.method == 'POST':
        form = CalendarEventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.author = request.user
            event.save()
            # Handle successful form submission, e.g., redirect
            return redirect('calendar_management')
    else:
        form = CalendarEventForm()

    return render(request, 'calendar_management.html', {'form': form, 'events': events,'user': request.user,'today': today} )

@login_required
def attended_event_list(request):
    events = CalendarEvent.objects.all()
    today = timezone.now()  # Format the date as needed
    now = timezone.now()
    return render(request, 'completed_event_list.html', {'events': events,'user': request.user,'today': today} )

@login_required
def edit_event(request, event_id):

    event = get_object_or_404(CalendarEvent, pk=event_id)

    if request.method == 'POST':
        form = CalendarEventForm(request.POST, instance=event)  # Pre-populate the form
        if form.is_valid():
            form.save()
            return redirect('calendar_management')  # Redirect to your event list URL
        else:
            # Handle form validation errors (optional: display them in the template)
            return render(request, 'edit_event.html', {'form': form, 'event': event})

    else:
        form = CalendarEventForm(instance=event)  # Create form with existing data

    return render(request, 'edit_event.html', {'form': form, 'event': event})
