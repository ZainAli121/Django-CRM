from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from . import models
from .models import Record

# Create your views here.
def home(request):
    records = Record.objects.all()
    if request.user.is_anonymous:
        return redirect('login')
    
    return render(request, 'home.html', {'records': records})

def signup_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        # check if user already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('signup')
        
        # create user
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            messages.success(request, 'User created successfully.')
    return render(request, 'signup.html', {})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # authenticate user
        user = authenticate(request, username=username, password=password)

        # check if user exists
        if user is not None:
            login(request, user)
            messages.success(request, 'User logged in successfully.')
            return redirect('/')
        else:
            messages.error(request, 'Invalid credentials.')
            return redirect('login')
        
    return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, 'User logged out successfully.')
    return redirect('login')