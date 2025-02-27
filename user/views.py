from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from  .models import User
from functools import wraps
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from django.contrib import messages
from django.urls import reverse
from .utils import send_email

def home(request):
    return render(request, 'home.html')

def register_view(request):
    if request.method== 'POST':
        username = request.POST.get("username")
        email= request.POST.get("email")
        password = request.POST.get("password")
        
        User.objects.create_user(username=username, email=email, password=password)
        
        return redirect('login')

    return render (request, 'register_user.html')


def login_view(request):
    if request.method== 'POST':
        username= request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Invalid username or password")
            return redirect('login')
            
        login(request, user)
        return redirect('dashboard')

    if request.user.is_authenticated:
        messages.info(request, f"You are already connectes as, {request.user.username}")
        return redirect('dashboard')
            
    return render (request, 'login_user.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def forgot_password(request):
    if request.method=='POST':
        email = request.POST.get("email")
        user = User.objects.get(email=email)

        if user is not None:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_url = request.build_absolute_uri(
                reverse('reset_password', kwargs={'uidb64': uid, 'token': token})
            )

            send_email(user, settings.DEFAULT_FROM_EMAIL, subject="Reset Password", template_name="email/send_reset_link.html", reset_url=reset_url)
            messages.success(request, "We have sent a reset link to your email!")
            return redirect('forgot_password')
        
        messages.error(request, "No user was found with that email!")
        return redirect('forgot_password')
    
    return render(request, 'forgot_password.html')

def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method=='POST':
            new_password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")

            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                
                messages.success(request, "Your password has been reset successfully!")
                return redirect('login')
            
            messages.info(request, "Passwords do not match")
            return redirect('reset_password')
            
        return render(request, "reset_password.html")
    
    messages.error(request, "The password reset link is invalid or has expired")
    return redirect('forgot_password')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

