from django.conf.urls import url
from apiserv.views import (
    register, event_req, event_details, user_details, generate_certificate
)
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

urlpatterns = [
    url('^api/register$', register),
    url('^api/events$', event_req),
    url('^api/events/(?P<pk>[0-9]+)$', event_details),
    url('^api/user$', user_details),
    url('^api/auth/login$', obtain_jwt_token),
    url('^api/auth/refresh-token$', refresh_jwt_token),
    url('^api/generate_certificate$', generate_certificate),
]
