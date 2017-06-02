from django.conf.urls import url
from api import api_views, views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^api-devices/$', api_views.DeviceList.as_view()),
    url(r'^api-devices/(?P<device_id>[\w-]+)/$', api_views.DeviceDetails.as_view()),
    url(r'^api-device-history/(?P<device_id>[\w-]+)/$', api_views.device_history),
    url(r'^$', views.redirect_to),
    url(r'^sign-in/$', views.user_login, name='login'),
    url(r'^sign-out/$', views.user_logout, name='logout'),
    url(r'^devices/$', views.devices),
    url(r'^devices/(?P<lab>[\w-]+)/$', views.devices),
    url(r'^device/(?P<slug>[\w-]+)/$', views.device_details),
    url(r'^home/$', views.home, name='home'),
    url(r'^search/', views.search, name='search'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
