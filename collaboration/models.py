from django.db import models
from django.conf import settings
from cloud.models import Folder
from user.models import User

class Collaboration(models.Model):
    collaborator= models.ForeignKey(User, on_delete=models.CASCADE)
    owner= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owned_collaborations", default=None)
    folder= models.ForeignKey(Folder, on_delete=models.CASCADE, related_name="share_collaborations")
    created_at = models.DateTimeField(auto_now_add=True)

class Invitation(models.Model):
    email= models.CharField(max_length= 255)
    status= models.CharField(max_length= 8, choices= [('ACCEPTED','accepted'),('REFUSED','refused')])
    owner=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    folder=models.ForeignKey(Folder, on_delete=models.CASCADE)

