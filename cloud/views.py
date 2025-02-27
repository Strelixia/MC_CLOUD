from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Folder, File
from django.http import JsonResponse
from django.contrib import messages
import cloudinary.uploader
from .forms import FileUploadForm
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import datetime


@login_required
def dashboard(request):
    # Récupère le dossier personnel de l'utilisateur (créé à la connexion via le signal)
    folder = get_object_or_404(Folder, user=request.user)
    
    # Si vous conservez les enregistrements des fichiers dans votre base de données :
    files = folder.files.all()
    
    return render(request, 'dashboard.html', {
        'folder': folder,
        'files': files
    })


@login_required
def upload_file(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, user=request.user)
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Téléverse le fichier sur Cloudinary dans un dossier spécifique
            uploaded = cloudinary.uploader.upload(
                request.FILES['file'],
                folder=folder.full_path() 
            )
            # Crée un nouvel enregistrement File avec les données téléversées
            new_file = form.save(commit=False)
            new_file.folder = folder
            new_file.name = form.cleaned_data['name']
            new_file.file = uploaded.get('public_id')  # Vous pouvez stocker le public_id ou l'URL selon vos besoins
            new_file.save()
            # Envoi d'une notification au groupe de l'utilisateur via Channels
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"user_{request.user.id}",
                {
                    "type": "send_update",
                    "message": "Nouveau fichier téléversé"
                }
            )
            return redirect('dashboard')
    else:
        form = FileUploadForm()
    return render(request, 'upload_file.html', {'form': form, 'folder': folder})


@login_required
def create_subfolder(request, parent_id):
    parent = get_object_or_404(Folder, id=parent_id, user=request.user)
    if request.method == "POST":
        subfolder_name = request.POST.get("name")
        if subfolder_name:
            Folder.objects.create(user=request.user, name=subfolder_name, parent=parent)
            return redirect('dashboard')
    folder=Folder.objects.all()
    return render(request, 'create_subfolder.html', {'parent': parent, 'folder': folder})


@login_required
def upload_file_selection(request):
    folder_id = request.GET.get('folder_id')
    if folder_id:
        return redirect('upload_file', folder_id=folder_id)
    return redirect('dashboard')
