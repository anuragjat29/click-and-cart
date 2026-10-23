from django.shortcuts import render, redirect
from .forms import RegisterForm
from .forms import LoginForm
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html',{"form":form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':

        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')

    else: form = LoginForm(request)
    return render(request, 'login.html',{'form':form})

@login_required
def logout_view(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            logout(request)
            messages.success(request, "Logged out successfully.")

        return redirect('login')

    return redirect('login')