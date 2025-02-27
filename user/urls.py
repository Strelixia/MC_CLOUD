from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("login/", views.login_view, name='login'),
    path("logout/", views.logout_view, name='logout'),
    path("register/", views.register_view, name='register'),
    path("forgot_password/", views.forgot_password, name ='forgot_password'),
    path("reset_password/<uidb64>/<token>", views.reset_password, name ='reset_password'),
]