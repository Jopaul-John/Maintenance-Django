from rest_framework import serializers
from api.models import Device, DeviceHistory


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        exclude = ('is_active', 'id', )


class DeviceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceHistory
        exclude = ()
