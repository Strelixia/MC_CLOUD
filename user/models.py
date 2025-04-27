"""
    Models for MC Cloud application
"""

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
        Class User: username, email, password
    """
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField('auth.Group', related_name= 'custom_user_groups', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name= 'custom_user_permissions', blank=True)

    def get_folder_permission(self, folder):
        if folder.user == self:
            return 'owner' 
        collab = self.collaborator_collaborations.filter(folder = folder).first()
        return collab.permission if collab else None
    
    def __str__(self):
        return f"Username: {self.username}, email: {self.email}"
    