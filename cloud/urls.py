from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name ='dashboard'),
    path('upload_file/<int:folder_id>/', views.upload_file, name='upload_file'),
    path('delete_file/', views.delete_file, name='delete_file'),
    # path('folder/<int:parent_id>/create_subfolder/', views.create_subfolder, name='create_subfolder'),
    path('create_subfolder_ajax/', views.create_subfolder_ajax, name='create_subfolder_ajax'),
]