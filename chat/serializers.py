from chat.models import Message,Chat
from rest_framework import serializers

class ChatListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Chat
        fields=('id','users')

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model=Message
        fields=('id','user_from','message_body')
