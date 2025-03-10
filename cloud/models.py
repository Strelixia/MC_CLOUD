import cloudinary.uploader
from django.db import models
import cloudinary
from django.contrib.auth import get_user_model
from django.conf import settings
from cloudinary.models import CloudinaryField


class Folder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="folders")
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subfolders')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.full_path()
    
    def full_path(self):
        if self.parent:
            return f"{self.parent.full_path()}/{self.name}"
        return self.name

class File(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name="files")
    name = models.CharField(max_length=255,null=True)
    file = CloudinaryField('file')  
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)



    