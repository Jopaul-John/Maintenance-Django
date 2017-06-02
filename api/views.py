from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from api.models import Device, DeviceHistory, Location, UserProfile
from django.contrib.auth.models import User
from django.contrib import messages


def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/home/')

    invalid = True
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            invalid = False
            if user.is_active:
                login(request, user)
                print('Success!')
                return HttpResponseRedirect('/home/')
            else:
                return HttpResponse("Your account has been deactivated.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            messages.error(request, 'Invalid credentials supplied.')
            return render(request, 'signin.html', {'invalid': invalid, }, )
    else:
        return render(request, 'signin.html', {})


def redirect_to(request):
    return HttpResponseRedirect('/sign-in/')


@login_required(login_url='/sign-in/')
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/sign-in/')


@login_required(login_url='/sign-in/')
def home(request):
    issues = DeviceHistory.objects.filter(is_active=True, resolved=False).order_by('-timestamp')[:5]
    resolved = DeviceHistory.objects.filter(is_active=True, resolved=True).order_by('-timestamp')[:5]
    return render(request, 'home.html', {'issues': issues, 'resolved': resolved})


@login_required(login_url='/sign-in/')
def search(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        devices = Device.objects.filter(device_id__icontains=q, is_active=True)
        if not devices:
            devices = Device.objects.filter(model__icontains=q, is_active=True)
        return render(request, 'search.html', {'devices': devices})


@login_required(login_url='/sign-in/')
def device_details(request, slug):
    device = get_object_or_404(Device, slug=slug, is_active=True)
    complaints = DeviceHistory.objects.filter(device=device, is_active=True)
    count = complaints.count()
    return render(request, 'device_details.html', {'device': device, 'complaints': complaints, 'count': count})


@login_required(login_url='/sign-in/')
def devices(request, lab=None):
    if lab:
        location = get_object_or_404(Location, name=lab)
        working = Device.objects.filter(location=location, status=True)
        working_count = working.count()
        defective = Device.objects.filter(location=location, status=False)
        defective_count = defective.count()
        return render(request, 'devices.html', {'working': working, 'working_count': working_count,
                                                'defective': defective, 'defective_count': defective_count,
                                                'lab': 'Displaying devices in ' + lab})

    else:
        working = Device.objects.filter(status=True)
        working_count = working.count()
        defective = Device.objects.filter(status=False)
        defective_count = defective.count()
        return render(request, 'devices.html', {'working': working, 'working_count': working_count,
                                                'defective': defective, 'defective_count': defective_count})
