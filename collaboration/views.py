from django.shortcuts import render redirect, get_object_or_404
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





@login_required
def collaboration(request):
    if request.method=='POST':  
        email = request.POST.get("email")
        collaborator = User.objects.get(email=email)

        if user is not None:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_url = request.build_absolute_uri(
                reverse('reset_password', kwargs={'uidb64': uid, 'token': token})
            )

            send_email(user, settings.DEFAULT_FROM_EMAIL, subject="Reset Password", template_name="email/send_reset_link.html", reset_url=reset_url)
            messages.success(request, "We have sent a reset link to your email!")
            return redirect('forgot_password')
    
    return render(request, 'forgot_password.html')
