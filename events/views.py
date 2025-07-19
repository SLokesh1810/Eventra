from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import profile, Event
from django.contrib import messages
from datetime import datetime

# Home view
def index(request):
    if request.user.is_authenticated:
        email = request.user.email
        user = User.objects.get(email=email)
        prof, _ = profile.objects.get_or_create(user=user)

        upcoming_events = Event.objects.filter(last_date_for_reg__gte=datetime.now(), is_approved=True)
        live_events = Event.objects.filter(date=datetime.now(), is_approved=True)
        return render(request, 'home.html', {'role': prof.role, 'user': user, 'upcoming_events': upcoming_events, 'live_events': live_events})
    
    return render(request, 'home.html')

# Login view
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': 'User does not exist'})

        username = user_obj.username
        user = authenticate(request, username=username, password=password)

        if user is not None:
            prof, _ = profile.objects.get_or_create(user=user)
            if not prof.is_approved:
                return render(request, 'login.html', {'error': 'Your account is not approved yet.'})

            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

# Signup view
def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'This email is already registered'})

        user = User.objects.create_user(username=username, email=email, password=password)
        approval = False if role == 'organiser' else True
        profile.objects.create(user=user, role=role, is_approved=approval)
        user.save()
        return redirect('login')
    return render(request, 'signup.html')

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')

# Create event view
def create_event_view(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to create events.")
            return redirect('login')

        prof, _ = profile.objects.get_or_create(user=request.user)
        if prof.role != 'organiser':
            messages.error(request, "You are not authorized to create events.")
            return redirect('index')

        try:
            event_name = request.POST.get('event_name')
            event_description = request.POST.get('event_description')
            event_date = request.POST.get('event_date')
            event_start_time = request.POST.get('event_start_time')
            event_fee = request.POST.get('event_fee', 0.00)
            event_mode = request.POST.get('event_mode')
            event_location_or_link = request.POST.get('event_location_or_link')
            duration_minutes = request.POST.get('event_duration', 60)
            event_image = request.FILES.get('event_image')

            event_datetime = datetime.fromisoformat(event_date)

            event = Event.objects.create(
                title=event_name,
                description=event_description,
                date=event_datetime,
                start_time=event_start_time,
                duration=duration_minutes,
                fee=event_fee,
                image=event_image,
                mode=event_mode,
                location_or_link=event_location_or_link,
                provider=request.user,
                is_approved=False
            )

            messages.success(request, "Event created successfully and sent for approval.")
            return redirect('index')

        except Exception as e:
            messages.error(request, f"Error creating event: {e}")
            return redirect('create_event')

    return render(request, 'create_event.html')

# View for admin approval dashboard
def approval_view(request):
    prof, _ = profile.objects.get_or_create(user=request.user)
    if prof.role == 'admin':
        users = User.objects.filter(profile__role='organiser', profile__is_approved=False)
        events = Event.objects.filter(is_approved=False)
        return render(request, 'approval.html', {'users': users, 'events': events})
    else:
        return HttpResponse("You are not authorized to view this page.")

def approve_all(request):
    if request.method == 'POST':
        # Handle organiser approvals
        pending_profiles = profile.objects.filter(is_approved=False, role='organiser')
        for prof in pending_profiles:
            user_id = prof.user.id
            decision = request.POST.get(f'approval_{user_id}')
            if decision == 'approve':
                prof.is_approved = True
            else:
                prof.is_approved = False
            prof.is_organiser_pending = False
            prof.save()

        # Handle event approvals
        pending_events = Event.objects.filter(is_approved=False)
        for event in pending_events:
            event_id = event.id
            decision = request.POST.get(f'event_approval_{event_id}')
            if decision == 'approve':
                event.is_approved = True
            else:
                event.is_approved = False
            event.save()

        messages.success(request, "All approvals submitted successfully.")
        return redirect('approval')
