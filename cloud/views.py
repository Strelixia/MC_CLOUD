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
from redis.exceptions import ConnectionError
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json


@login_required
def dashboard(request):
    folder = get_object_or_404(Folder, user=request.user, parent=None)

    subfolders = Folder.objects.filter(user=request.user, parent=folder)
    
    files = folder.files.all()

    form = FileUploadForm()
    
    return render(request, 'dashboard.html', {
        'folder': folder,
        'files': files,
        'subfolders': subfolders,
        'form': form
    })


@login_required
def upload_file(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, user=request.user)
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded = cloudinary.uploader.upload(
                request.FILES['file'],
                folder=folder.full_path() 
            )

            new_file = form.save(commit=False)
            new_file.folder = folder
            new_file.name = form.cleaned_data['name']
            new_file.file = uploaded.get('public_id')
            new_file.save()

            channel_layer = get_channel_layer()
            try:
                async_to_sync(channel_layer.group_send)(
                    f"user_{request.user.id}",
                    {
                        "type": "send_update",
                        "message": "Nouveau fichier téléversé"
                    }
                )
            except ConnectionError:
                messages.error(request, "Failed to send notification. Redis server might be down.")
            return redirect('dashboard')
        else:
            messages.error(request, "File upload failed. Ensure the file is an image and less than 10MB.")
    return redirect('dashboard')


@login_required
def delete_file(request):
    if request.method == 'POST':
        file_id = json.loads(request.body).get('file_id')
        file = get_object_or_404(File, id=file_id)
        try:
            cloudinary.uploader.destroy(file.file.public_id)
            file.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False})


@login_required
@csrf_exempt
def create_subfolder(request):
    if request.method == "POST":
        data = json.loads(request.body)
        parent_id = data.get('parent_id')
        subfolder_name = data.get('name')
        parent = get_object_or_404(Folder, id=parent_id, user=request.user)
        if subfolder_name:
            existing_folder = Folder.objects.filter(user=request.user, name=subfolder_name, parent=parent).first()
            if not existing_folder:
                new_folder = Folder.objects.create(user=request.user, name=subfolder_name, parent=parent)

                cloudinary.uploader.upload(
                    "https://res.cloudinary.com/demo/image/upload/sample.jpg",
                    folder=new_folder.full_path()
                )
                return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required
def folder_detail(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, user=request.user)
    subfolders = Folder.objects.filter(user=request.user, parent=folder)
    files = folder.files.all()
    form = FileUploadForm()

    return render(request, 'folder_detail.html', {
        'folder': folder,
        'files': files,
        'subfolders': subfolders,
        'form': form
    })


@login_required
def collaboration(request):
    if request.method=='POST':
        