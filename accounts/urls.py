"""
URL configuration for the accounts app.

This module defines URL patterns for authentication functionality:
- Registration, login, logout
- Profile management
- User dashboard
"""

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    # Registration
    path('register/', views.register_view, name='register'),
    
    # Login/Logout - using Django's built-in views
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Profile management
    path('profile/', views.profile_view, name='profile'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # Password management (optional - using Django's built-in views)
    path('password-change/', 
         auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html'),
         name='password_change'),
    path('password-change/done/', 
         auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),
         name='password_change_done'),
]