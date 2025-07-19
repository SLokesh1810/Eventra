from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import profile

# Create your views here.
def index(request):
    return render(request, 'home.html')

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
            prof,_ = profile.objects.get_or_create(user=user)
            if not prof.is_approved:
                return render(request, 'login.html', {'error': 'Your account is not approved yet.'})

            login(request, user)  
            return redirect('index')  

        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


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
        profile.objects.create(user=user,role=role,is_approved=approval)
        user.save()
        
        
        return redirect('login')  

    return render(request, 'signup.html')


def logout_view(request):
    logout(request)
    return redirect('login')

