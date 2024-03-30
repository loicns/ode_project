from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),  # Example for home_view
    path('upload/', views.UploadView.as_view(), name='upload'),
    path('success/', views.success_view, name='success'),
]
