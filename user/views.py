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
    # Store the 'next' parameter if it exists in the URL
    next_url = request.GET.get('next', '')
    if next_url:
        request.session['next_url'] = next_url
        
    if request.method== 'POST':
        username = request.POST.get("username")
        email= request.POST.get("email")
        password = request.POST.get("password")
        
        user = User.objects.create_user(username=username, email=email, password=password)
        
        # Log the user in immediately after registration
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            
            # Redirect to stored next_url if it exists, otherwise to dashboard
            next_url = request.session.get('next_url')
            if next_url:
                del request.session['next_url']
                return redirect(next_url)
            return redirect('dashboard')
            
        return redirect('login')

    return render(request, 'register_user.html', {'next_url': next_url})


def login_view(request):
    # Get next_url from URL parameters
    next_url = request.GET.get('next', '')
    
    if request.method== 'POST':
        username= request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Invalid username or password")
            # Preserve next parameter on error
            return redirect(f"{reverse('login')}?next={next_url}" if next_url else 'login')
            
        login(request, user)
        
        # Redirect to next_url if it exists
        if next_url:
            return redirect(next_url)
        return redirect('dashboard')

    if request.user.is_authenticated:
        messages.info(request, f"You are already connected as, {request.user.username}")
        return redirect('dashboard')
    
    return render(request, 'login_user.html', {'next_url': next_url})

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
                reverse('reset_password', kwargs={'uidb64': uid, 'token': token}))

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

