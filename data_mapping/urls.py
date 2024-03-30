from django.urls import path
from . import views  # Import views from the same app

app_name = 'data_mapping'

urlpatterns = [
  path('data/process/', views.process_data, name='process'),
  path('mapping/', views.mapping_view, name='mapping_view'),
]
