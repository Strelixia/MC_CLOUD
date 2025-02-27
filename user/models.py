"""
    Models for MC Cloud application
"""

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
        Class User: username, email, password
    """
    groups = models.ManyToManyField('auth.Group', related_name= 'custom_user_groups', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name= 'custom_user_permissions', blank=True)

    def __str__(self):
        return f"Username: {self.username}, email: {self.email}"
    