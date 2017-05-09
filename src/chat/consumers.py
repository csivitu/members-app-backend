from chat.auth_decorators import jwt_authenticate,close_conn
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
    user_obj = User.objects.get(username=user)
    chat_array = Chat.objects.filter(users=user_obj)
    chat_list_response = ChatListSerializer(chat_array,many=True)
    ret_obj = {"Chats":chat_list_response.data}
    message.reply_channel.send({"text":json.dumps(ret_obj)})


@channel_session
@jwt_authenticate
def chat_connect(message):

    user = message.channel_session['user']
    user_obj = User.objects.get(username=user)
    chat_id = message.channel_session['chatid']
    last_message_id = message.channel_session['last_msg_id']
    chat_obj = Chat.objects.get(pk=chat_id,users=user_obj)
    if chat_obj is None:
        close_conn(message)

    unread_messages = Message.objects.filter(chat=chat_obj,pk__gt=last_message_id)
    message_response = MessageSerializer(unread_messages,many=True)
    retObj = {"Messages":message_response.data}

    message.reply_channel.send({"text":json.dumps(retObj)})
    Group("chat_"+chat_id).add(message.reply_channel)


@channel_session
@jwt_authenticate
def chat_message(message):
    user = message.channel_session['user']
    user_obj = User.objects.get(username=user)
    chat_id = message.channel_session['chatid']
    message_body = message.content['text']
    chat_obj = Chat.objects.get(pk=chat_id,users=user_obj)
    msg = chat_obj.add_message(user_from=user_obj,message_body=message_body)
    msg_return = MessageSerializer(msg)
    Group("chat_"+chat_id).send({"text":json.dumps(msg_return.data)})

@channel_session
@jwt_authenticate
def chat_disconnect(message):
    chatid = message.channel_session['chatid']
    Group("chat_"+chatid).discard(message.reply_channel)
    close_conn(message)