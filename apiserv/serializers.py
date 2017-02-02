from rest_framework import serializers
from apiserv.models import *
#from django.contrib.auth.models import User


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('id', 'date', 'name', 'venue', 'cat','time')

class EventCompSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('id', 'date', 'name', 'venue', 'cat','desc','images','link','time')

class UserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('name', 'username', 'phone', 'mem_type', 'email')

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('name', 'username', 'phone', 'password', 'email')
    
    def create(self, validated_data):
        return User.objects.create(**validated_data)
