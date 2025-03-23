from django.urls import path
from . import views

urlpatterns = [
    path("make_collaboration/", views.make_collaboration, name ='make_collaboration'),
    path("accept_invite/<uidb64>/<token>", views.accept_invite, name ='accept_invite'),
]