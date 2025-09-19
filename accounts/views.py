"""
Authentication views for the Django blog application.

This module provides simplified authentication functionality:
- User registration with basic form
- Login/logout using Django's built-in authentication
- Profile management
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile


def register_view(request):
    """
    User registration view using Django's built-in UserCreationForm.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('accounts:login')
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """
    Custom login view (optional - can use Django's built-in LoginView).
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('accounts:dashboard')  # Redirect to home page or dashboard
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'accounts/login.html')


@login_required
def profile_view(request):
    """
    User profile view to display and edit basic profile information.
    """
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        # Create profile if it doesn't exist
        profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        # Simple profile update
        bio = request.POST.get('bio', '')
        profile.bio = bio
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('accounts:profile')
    
    context = {
        'user': request.user,
        'profile': profile,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def dashboard_view(request):
    """
    Simple user dashboard showing basic information.
    """
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    context = {
        'user': request.user,
        'profile': profile,
    }
    return render(request, 'accounts/dashboard.html', context)
