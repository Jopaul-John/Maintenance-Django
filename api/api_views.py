from api.models import Device, DeviceHistory
from api.serializers import DeviceSerializer, DeviceHistorySerializer
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse

# TODO: View for user list


class DeviceList(generics.ListCreateAPIView):
    """
    View for listing and creating Device instances.
    """
    lookup_field = 'device_id'
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class DeviceDetails(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, destroying Device instances.
    """
    lookup_field = 'device_id'
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


@api_view(['GET', ])
def device_history(request, device_id):
    try:
        device = Device.objects.get(device_id=device_id)
        print('Found!')
    except Device.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        history = device.history.all().order_by('-id')
        print(history)
        serializer = DeviceHistorySerializer(history, many=True)
        return Response(serializer.data)
