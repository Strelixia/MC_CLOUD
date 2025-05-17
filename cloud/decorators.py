from functools import wraps
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from collaboration.models import Folder, Collaboration

def permission_required():
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, folder_id, *args, **kwargs):
            folder = get_object_or_404(Folder, id=folder_id)

            if folder.user == request.user:
                return view_func(request, folder_id, *args, **kwargs)
            current_folder = folder
            while current_folder is not None:
                try:
                    collaboration = Collaboration.objects.get(folder=folder, collaborator=request.user)
                    if collaboration.permission in ['read', 'write']:
                        return view_func(request, folder_id, *args, **kwargs)
                except Collaboration.DoesNotExist:
                    pass
                current_folder = current_folder.parent
            return HttpResponseForbidden("You don't have permission to access this resource.")
                    
        return _wrapped_view
    return decorator 


