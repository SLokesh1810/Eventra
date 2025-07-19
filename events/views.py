from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'templates/home.html')

def login(request):
    return render(request, 'templates/login.html')

def signup(request):
    return render(request, 'templates/signup.html')