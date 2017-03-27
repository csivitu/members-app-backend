from chat.auth_decorators import jwt_authenticate
from chat.serializers import ChatListSerializer,MessageSerializer
from channels.sessions import channel_session,enforce_ordering
from chat.models import Chat,Message
from django.contrib.auth import get_user_model
from channels import Group
import ujson as json

User = get_user_model()


@channel_session
@jwt_authenticate
def chat_list(message):
    user = message.channel_session['user']
    userObj = User.objects.get(username=user)
    ChatArray = Chat.objects.filter(users=userObj)
    ChatListRespnse = ChatListSerializer(ChatArray,many=True)
    retObj = {"Chat":ChatListRespnse.data}
    message.reply_channel.send({"text":json.dumps(retObj)})


@channel_session
@jwt_authenticate
def chat_connect(message):
    user = message.channel_session['user']
    chatid = message.channel_session['chatid']
    lastMessageId = message.channel_session['lastmsgid']
    ChatObj = Chat.objects.get(pk=chatid)
    UnreadMessages = Message.objects.filter(chat=ChatObj,pk__gt=lastMessageId)
    MessageResponse = MessageSerializer(UnreadMessages,many=True)
    retObj = {"Messages":MessageResponse.data}

    message.reply_channel.send({"text":json.dumps(retObj)})
    Group("chat_"+chatid).add(message.reply_channel)


@channel_session
@jwt_authenticate
def chat_message(message):
    user=message.channel_session['user']
    userObj=User.objects.get(username=user)
    chatid=message.channel_session['chatid']
    message_body=message.content['text']
    ChatObj=Chat.objects.get(pk=chatid)
    ChatObj.add_message(user_from=userObj,message_body=message_body)
    Group("chat_"+chatid).send({"text":message_body})

@channel_session
@jwt_authenticate
def chat_disconnect(message):
    chatid=message.channel_session['chatid']
    Group("chat_"+chatid).discard(message.reply_channel)
