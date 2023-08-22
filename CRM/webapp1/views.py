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


def user_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'record': record})
    
    else:
        messages.success(request, 'Please login to view this page.')
        return redirect('login')
    
def delete_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        record.delete()
        messages.success(request, 'Record deleted successfully.')
        return redirect('/')
    
    else:
        messages.success(request, 'Please login to view this page.')
        return redirect('login')
    

def add_record(request):
    if request.user.is_anonymous:
        messages.success(request, 'Please login to view this page.')
        return redirect('login')     
    else:
        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            phone_number = request.POST['phone_number']
            email = request.POST['email']
            address = request.POST['address']
            city = request.POST['city']
            state = request.POST['state']
            zipcode = request.POST['zipcode']
    
            record = Record.objects.create(first_name=first_name, last_name=last_name, phone_number=phone_number, email=email, address=address, city=city, state=state, zipcode=zipcode)
            record.save()
            messages.success(request, 'Record added successfully.')
            return redirect('/')
    return render(request, 'add_record.html', {})

def update_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        if request.method == 'POST':
            record.first_name = request.POST['first_name']
            record.last_name = request.POST['last_name']
            record.phone_number = request.POST['phone_number']
            record.email = request.POST['email']
            record.address = request.POST['address']
            record.city = request.POST['city']
            record.state = request.POST['state']
            record.zipcode = request.POST['zipcode']
            record.save()
            messages.success(request, 'Record updated successfully.')
            return redirect('/')
        
        else:
            initial_data = {
                'first_name': record.first_name,
                'last_name': record.last_name,
                'phone_number': record.phone_number,
                'email': record.email,
                'address': record.address,
                'city': record.city,
                'state': record.state,
                'zipcode': record.zipcode

            }

            return render(request, 'update_record.html', {'record': record, 'initial_data': initial_data})