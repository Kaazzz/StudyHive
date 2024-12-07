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
            return redirect('event_list')
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
    return redirect('event_list')  # Replace 'event_list' with your actual URL name

