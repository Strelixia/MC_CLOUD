from functools import wraps
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from .models import Folder, Collaboration

def permission_required(required_level='read'):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, folder_id, *args, **kwargs):
            folder = get_object_or_404(Folder, id=folder_id)

            if folder.owner == request.user:
                return view_func(request, folder_id, *args, **kwargs)

            try:
                collaboration = Collaboration.objects.get(folder=folder, collaborator=request.user)
                if required_level == 'read' and collaboration.permission in ['read', 'write']:
                    return view_func(request, folder_id, *args, **kwargs)
                elif required_level == 'write' and collaboration.permission == 'write':
                    return view_func(request, folder_id, *args, **kwargs)
            except Collaboration.DoesNotExist:
                pass

            return HttpResponseForbidden("Vous n'avez pas la permission d'accéder à cette ressource.")
        return _wrapped_view
    return decorator
