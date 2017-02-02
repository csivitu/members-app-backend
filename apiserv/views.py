import ujson as json
import hashlib
import traceback

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.response import Response

from apiserv.cert_gen import cert_gen
from apiserv.models import Event
from apiserv.serializers import (
    EventSerializer, EventCompSerializer, UserDetailsSerializer, UserSerializer
)


User = get_user_model()


@api_view(['GET'])
def generate_certificate(request):
    image = cert_gen(request.user.name, request.user.username,
                     request.user.date_joined.year)
    response = HttpResponse(content_type="image/jpeg")
    image.save(response, "JPEG")
    return response


@api_view(['GET'])
def event_req(request):
    if request.method == 'GET':
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def user_details(request):
    if request.method == 'GET':
        u = User.objects.get(username=request.user)
        serializer = UserDetailsSerializer(u)
        return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def register(request):
    try:
        jdata=json.loads(request.body)
        u = UserSerializer(data=jdata)
        if(u.is_valid(raise_exception=True)):

            if(jdata['mem_type']==1 or jdata['mem_type']==2):#If trying to register as paid or 2 credit course member
                request_key=jdata['key']

                #Generates a key by concating reg_no+mem_type+secret_key , hashing it and substring the first 8 chars
                secret=jdata['username'].upper()+str(jdata['mem_type'])+settings.SECRET_KEY
                generated_key=hashlib.sha1(secret.encode('utf-8')).hexdigest()[0:8]
                if(request_key!=generated_key):
                    return HttpResponse(json.dumps({'detail':'Invalid Key','code':'500'}),status=201)
                
            u.validated_data['password']= make_password(u.validated_data['password'])
            u.save()
            return HttpResponse(status=201)
    except Exception:
        traceback.print_exc()
        return HttpResponse(
            json.dumps({'detail': 'Internal error', 'code': '500'}),
            status=500
        )


@api_view(['GET'])
def event_details(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return HttpResponse(
            json.dumps({'detail': 'Event not found', 'code': '404'}),
            status=404
        )

    if request.method == 'GET':
        serializer = EventCompSerializer(event)
        return Response(serializer.data)
