from django.conf.urls import url
from apiserv.views import (
    register, event_req, event_details, user_details, generate_certificate
)
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

urlpatterns = [
    url('^user$', user_details),
    url('^register$', register),

    url('^events$', event_req),
    url('^events/(?P<pk>[0-9]+)$', event_details),

    url('^auth/login$', obtain_jwt_token),
    url('^auth/refresh-token$', refresh_jwt_token),

    url('^generate_certificate$', generate_certificate),
]
