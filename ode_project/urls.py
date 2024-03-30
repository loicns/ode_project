"""
URL configuration for ode_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from data_intake import views  # Import views from the data_intake app
from data_intake.urls import urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('data_intake.urls', 'data_intake'), namespace='data_intake')),
    path('upload/', views.UploadView.as_view(), name='upload'),
]

# Include URL patterns from other apps (e.g., data_mapping, data_visualization)
urlpatterns += [
  path('data_mapping/', include(('data_mapping.urls', 'data_mapping'), namespace='data_mapping')),
  # ... similar patterns for other apps
]
