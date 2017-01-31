from django.shortcuts import render
from django.conf import settings
import ujson,hashlib,jwt,datetime
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apiserv.models import *
from apiserv.serializers import EventSerializer
from apiserv.serializers import EventCompSerializer
from django.contrib.auth.models import User
from rest_framework.decorators import authentication_classes, permission_classes
import traceback

@api_view(['GET'])
def EventReq(request):
    if request.method == 'GET':
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def register(request):
    try:
        jdata=ujson.loads(request.body)
        user = User.objects.create_user(username = jdata["regno"],password = jdata["password"],email=jdata["email"])
        user.save()
        profile=Profile.objects.get(user=user)
        profile.name=jdata["name"]
        profile.phone=jdata["phone"]
        profile.save()
        return HttpResponse(status=200)
    except Exception:
        traceback.print_exc()
        return HttpResponse(status=500)
    


@api_view(['GET'])
def EventDetails(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = EventCompSerializer(event)
        return Response(serializer.data)
