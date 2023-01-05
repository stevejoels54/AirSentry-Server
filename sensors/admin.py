from django.contrib import admin
from .models import Device, Reading, Notification

# Register your models here.

admin.site.register(Device)
admin.site.register(Reading)
admin.site.register(Notification)
