from cloud.models import Folder
from  .models import Invitation, Collaboration
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from django.contrib import messages
from django.urls import reverse
from .utils import send_email
from django.urls import reverse
from django.utils.http import urlencode


@login_required
def make_collaboration(request):
    if request.method=='POST':  
        collaborator_email = request.POST.get("email")
        folder_id = request.POST.get("folder_id")
        permission = request.POST.get("permission")
        folder = Folder.objects.filter(id=folder_id).first()
        owner = request.user
        print("Permission avant invitation:",permission)

        invitation = Invitation.objects.create(collaborator_email = collaborator_email,status = "PENDING", owner = owner, folder = folder, permission = permission)

        uid = urlsafe_base64_encode(force_bytes(invitation.pk))
        token = invitation.generate_token()

        inviting_url = request.build_absolute_uri(
            reverse('accept_invite', kwargs={'uidb64': uid, 'token': token})
        )
        
        send_email(owner, collaborator_email, subject="collaboration invitation", template_name="email/invitation_link.html", inviting_url=inviting_url)
        messages.success(request, "We have sent a inviting link to the collaborator email!")
        return redirect('make_collaboration')
    
    return render(request, 'make_collab.html', {'folders': Folder.objects.filter(user=request.user)})


@login_required
def accept_invite(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        invitation = get_object_or_404(Invitation, pk=uid)
    except Exception:
        invitation = None
        
    if invitation is not None and invitation.check_token(token):
        # If user is not authenticated, redirect to register with next parameter
        if not request.user.is_authenticated:
            base_url = reverse('register')
            query_params = urlencode({'next': request.get_full_path()})
            return redirect(f"{base_url}?{query_params}")
            
        if request.user.email != invitation.collaborator_email:
            messages.error(request, "You are not authorized to accept this invitation.")
            return redirect('dashboard')

        if invitation.status == "ACCEPTED":
            messages.info(request, "You have already accepted this invitation.")
            return redirect('dashboard')

        if request.method == "POST":
            status = request.POST.get("status")
            if status == "ACCEPTED":
                print("Permission avant collaboration:", invitation.permission)
                Collaboration.objects.create(collaborator=request.user, owner=invitation.owner, folder=invitation.folder, permission=invitation.permission )
                messages.success(request, "You have successfully joined the collaboration!")
            else:
                messages.info(request, "You declined the invitation.")

            invitation.status = status
            invitation.save()
            return redirect('dashboard')
        
        return render(request, "accept_invite.html", {"invitation": invitation})

    messages.error(request, "Invalid or expired invitation link.")
    return redirect('dashboard')


