from rest_framework import serializers
from apiserv.models import *


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('id', 'date', 'name', 'venue', 'cat','time')

class EventCompSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('id', 'date', 'name', 'venue', 'cat','desc','images','link','time')