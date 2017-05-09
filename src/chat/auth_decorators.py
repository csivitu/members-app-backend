from functools import wraps
from rest_framework_jwt.utils import jwt_decode_handler
from django.contrib.auth import get_user_model
from chat.models import Chat
from django.core.exceptions import ObjectDoesNotExist

Users = get_user_model()


def parse_get(query):
    d={}
    if(query):
        for param in query.split("&"):
            param=param.split("=")
            d[param[0]]=param[1]
    return d

def authenticate(token,message):
    try:
        payload = jwt_decode_handler(token)
    except Exception:
        close_conn(message)
        msg = 'Token invalid/expired.'
        print(msg)
        raise ValueError(msg)
    user = payload['username']
    return user



def close_conn(message):
    message.reply_channel.send({'close': True})

def jwt_authenticate(func):
    @wraps(func)
    def inner(message):

        if 'user' in message.channel_session.keys():
            return func(message)

        query_string = message.content['query_string']
        params = parse_get(query_string)

        if 'token' not in params.keys():
            print('No token')
            close_conn(message)

        else:
            token = params['token']
            user = authenticate(token,message)
            message.channel_session['user'] = user

            if 'chat_id' and 'last_msg_id' in params.keys():
                chat_id = params['chat_id']
                msg_id = params['last_msg_id']
                message.channel_session['last_msg_id'] = msg_id
                message.channel_session['chatid'] = chat_id

            return func(message)
        close_conn(message)
    return inner
