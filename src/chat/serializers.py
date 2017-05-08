from chat.models import Message,Chat
from rest_framework import serializers

class ChatListSerializer(serializers.ModelSerializer):

    class Meta:
        model=Chat
        fields=('id','users_list')

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model=Message
        fields=('id','msg_from','message_body','timestamp')


