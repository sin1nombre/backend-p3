from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'index.html')

def register(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(username=email).exists():
            return render(request, 'register.html', {'error': 'Email already exists'})
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return redirect('/login/')
    return render(request, 'register.html')

def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/dashboard/')
        else:
            return render(request, 'login.html', {'error': 'Invalid email or password'})
    return render(request, 'login.html')

def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('/')

@login_required(login_url='/login/')
def dashboard(request: HttpRequest) -> HttpResponse:
    users = None
    if request.user.is_superuser:
        users = User.objects.all()

    return render(request, 'dashboard.html', {'users': users})

def change(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        new_email = request.POST.get('new_email')
        new_password = request.POST.get('new_password')
        try:
            user = User.objects.get(id=user_id)
            if new_email:
                user.email = new_email
                user.username = new_email
            if new_password:
                user.set_password(new_password)
            user.save()
            return redirect('/dashboard/')
        except User.DoesNotExist:
            return render(request, 'change.html', {'error': 'User does not exist'})
    return render(request, 'change.html')
