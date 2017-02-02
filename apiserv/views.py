import ujson as json

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse

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
        data = json.loads(request.body)
        u = UserSerializer(data=data)
        if u.is_valid(raise_exception=True):
            password = make_password(u.validated_data['password'])
            u.validated_data['password'] = password
            u.save()
            return HttpResponse(status=201)
    except Exception:
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
