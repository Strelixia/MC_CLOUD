from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name ='dashboard'),
    path('upload_file/<int:folder_id>/', views.upload_file, name='upload_file'),
    # path('subfolder/', views.create_subfolder, name='create_subfolder'),
    path('upload/select/', views.upload_file_selection, name='upload_file_selection'),
    path('folder/<int:parent_id>/create_subfolder/', views.create_subfolder, name='create_subfolder'),

]