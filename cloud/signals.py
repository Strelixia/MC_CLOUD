from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import Folder
import cloudinary
import cloudinary.uploader
from decouple import config


@receiver(user_logged_in)
def create_user_folder_on_login(sender, user, request, **kwargs):
    """"Lorsqu'un utilisateur se connecte, vérifie s'il a déjà un dossier personnel.
    Sinon, en crée un nommé d'après son nom d'utilisateur."""

    if not Folder.objects.filter(user=user).exists():
        folder = Folder.objects.create(user=user, name=user.username)

        cloudinary.uploader.upload(
            "https://res.cloudinary.com/demo/image/upload/sample.jpg",
            folder=user.username
        )