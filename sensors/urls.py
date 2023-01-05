from django.urls import path
from . import views

urlpatterns = [
    path('current/', views.current_reading, name='current'),
    path('readings/', views.readings, name='readings'),
    path('reading_details/<int:pk>/',
         views.reading_details,
         name='reading_details'),
    path('devices/', views.devices, name='devices'),
    path('device_details/<int:pk>/',
         views.device_details,
         name='device_details'),
    path('trends/', views.trends, name='trends'),
    path('notifications/', views.notifications, name='notifications'),
]