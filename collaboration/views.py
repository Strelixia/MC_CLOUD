from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from django.contrib import messages
from django.urls import reverse
from .utils import send_email
from  .models import Invitation
from cloud.models import Folder

@login_required
def make_collaboration(request):
    if request.method=='POST':  
        collaborator = request.POST.get("email")
        folder_id = request.POST.get("folder_id")
        folder = Folder.objects.filter(id=folder_id).first()
        owner = request.user
        
        invitation = Invitation.objects.create(collaborator = collaborator,status = "REFUSED", owner = owner, folder = folder)

        uid = urlsafe_base64_encode(force_bytes(invitation.pk))
        token = default_token_generator.make_token(invitation)
        inviting_url = request.build_absolute_uri(
            reverse('accept_invite', kwargs={'uidb64': uid, 'token': token})
        )
        
        send_email(owner, collaborator, subject="collaboration invitation", template_name="email/invitation_link.html", inviting_url=inviting_url)
        messages.success(request, "We have sent a inviting link to the collaborator email!")
        return redirect('make_collab')
    
    return render(request, 'make_collab.html', folders=Folder.objects.filter(owner=request.user))

@login_required
def accept_invite(request, uidb64, token):
    if request.method=='POST':
