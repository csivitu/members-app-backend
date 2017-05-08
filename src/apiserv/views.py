import ujson as json
import hashlib
import traceback

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.conf import settings

from rest_framework.decorators import api_view,authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from apiserv.cert_gen import cert_gen
from apiserv.models import Event
from apiserv.serializers import (
    EventSerializer, EventCompSerializer, UserDetailsSerializer, UserSerializer
)



jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER




User = get_user_model()

def valid_paid_key(data):
    request_key=data['key']
    #Generates a key by concating reg_no+mem_type+secret_key , hashing it and substring the first 8 chars
    secret=data['username'].upper()+str(data['mem_type'])+settings.SECRET_KEY
    generated_key=hashlib.sha1(secret.encode('utf-8')).hexdigest()[0:8]
    if(request_key!=generated_key):
        return False
    else:
        return True

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
        statusObj={"success":"True","message": "Events fetched", "code": "200"}
        return Response({"status":statusObj,"Events":serializer.data},status=200)


@api_view(['GET'])
def user_details(request):
    if request.method == 'GET':
        u = User.objects.get(username=request.user)
        rObj = UserDetailsSerializer(u).data
        statusObj={"status":{"success":"True","message": "User detail fetched", "code": "200"}}
        rObj.update(statusObj)
        return Response(rObj,status=200)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def register(request):
    try:
        jdata=json.loads(request.body)
        u = UserSerializer(data=jdata)

        if(u.is_valid(raise_exception=True)):
            if(jdata['mem_type']==1 or jdata['mem_type']==2):#Paid members
                if(valid_paid_key(jdata)==False):#Key check
                    statusObj={"success":"False","message": "Invalid Key", "code": "401"}
                    return HttpResponse(json.dumps({"status":statusObj}),status=401)


            u.validated_data['password']= make_password(u.validated_data['password'])
            registered_user=u.save()
            payload = jwt_payload_handler(registered_user)
            token = jwt_encode_handler(payload)
            statusObj={"success":"True","code":201,"message":"Registered"}
            return HttpResponse(json.dumps({"status":statusObj,"token":token}),status=201)

    except Exception:
        statusObj={"success":"False","message": "Internal error", "code": "500"}
        return HttpResponse(
            json.dumps({"status":statusObj},status=500),
            status=500
        )


@api_view(['GET'])
def event_details(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        statusObj={"success":"False","message": "Event not found", "code": "404"}
        return HttpResponse(json.dumps({"status":statusObj}),status=404)

    if request.method == 'GET':
        serializer = EventCompSerializer(event)
        rObj=serializer.data
        statusObj={"status":{"success":"True","message": "Event fetched", "code": "200"}}
        rObj.update(statusObj)
        return Response(rObj,status=200)
