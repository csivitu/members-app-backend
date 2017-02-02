from django.shortcuts import render
from django.conf import settings
import ujson,datetime
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apiserv.models import *
from apiserv.serializers import *
from rest_framework.decorators import authentication_classes, permission_classes
import traceback
from apiserv.cert_gen import cert_gen
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model



User = get_user_model()

@api_view(['GET'])
def generate_certificate(request):
    image=cert_gen(request.user.name,request.user.username,request.user.date_joined.year)
    response = HttpResponse(content_type="image/jpeg")
    image.save(response, "JPEG")
    return response

@api_view(['GET'])
def EventReq(request):
    if request.method == 'GET':
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def UserDetails(request):
    if request.method == 'GET':
        u = User.objects.get(username=request.user)
        serializer = UserDetailsSerializer(u)
        return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def register(request):
    try:
        jdata=ujson.loads(request.body)
        u = UserSerializer(data=jdata)
        if(u.is_valid(raise_exception=True)):
            u.validated_data['password']= make_password(u.validated_data['password'])
            u.save()
            return HttpResponse(status=201)
    except Exception:
        return HttpResponse(ujson.dumps({'detail':'Internal error','code':'500'}),status=500)


@api_view(['GET'])
def EventDetails(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return HttpResponse(ujson.dumps({'detail':'Event not found','code':'404'}),status=404)

    if request.method == 'GET':
        serializer = EventCompSerializer(event)
        return Response(serializer.data)
