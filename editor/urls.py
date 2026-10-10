from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_video, name='upload_video'),
    path('process/<int:pk>/', views.process_video, name='process_video'),
    path('edit/<int:pk>/', views.edit_video, name='edit_video'),
    path('delete/<int:pk>/', views.delete_video, name='delete_video'),
    path('download/<str:filename>/', views.download_file, name='download_file'),
]