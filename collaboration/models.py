from django.db import models
from django.conf import settings
from cloud.models import Folder
from user.models import User
import uuid
import hashlib

class Collaboration(models.Model):
    collaborator = models.ForeignKey(User, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owned_collaborations", default=None)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name="share_collaborations")
    created_at = models.DateTimeField(auto_now_add=True)
    permission = models.CharField(max_length=8, choices=[('READ','read'),('WRITE','write')], default='write')
    def __str__(self):
        return f'{self.collaborator}| {self.folder} ({self.permission})'

class Invitation(models.Model):
    collaborator_email = models.CharField(max_length= 255)
    status = models.CharField(max_length= 8, choices= [('PENDING','pending'),('ACCEPTED','accepted'),('REFUSED','refused')])
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    permission = models.CharField(max_length=8, choices=[('READ','read'),('WRITE','write')], default='write')
    
    def generate_token(self):
        unique_string = f"{self.pk}{self.collaborator_email}{self.created_at}{settings.SECRET_KEY}"
        return hashlib.sha256(unique_string.encode()).hexdigest()

    def check_token(self, token):
        return self.generate_token() == token
