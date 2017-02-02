from django.conf.urls import url
from . import views
from apiserv.views import *
from rest_framework_jwt.views import obtain_jwt_token,refresh_jwt_token

urlpatterns = [
   # url('^api/auth/login$', authLogin),
    url('^api/register$', register),
    url('^api/events$', EventReq),
    url('^api/events/(?P<pk>[0-9]+)$', EventDetails),
    url('^api/user$', UserDetails),
    url('^api/auth/login$', obtain_jwt_token),
    url('^api/auth/refresh-token$', refresh_jwt_token),
    url('^api/generate_certificate$', generate_certificate),
]
