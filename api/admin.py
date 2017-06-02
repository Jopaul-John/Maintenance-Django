from django.contrib import admin
from api.models import Device, DeviceHistory, Location

# Register your models here.

admin.site.register(Device)
admin.site.register(DeviceHistory)
admin.site.register(Location)
