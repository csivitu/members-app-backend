from django.conf.urls import url
from chat.views import chat_view

urlpatterns = [
    url('^core$', chat_view)
    ]