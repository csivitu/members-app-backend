from functools import wraps
from rest_framework_jwt.utils import jwt_decode_handler


def parse_get(query):
    d={}
    for param in query.split("&"):
        param=param.split("=")
        d[param[0]]=param[1]
    return d

def authenticate(token):
    try:
        payload = jwt_decode_handler(token)
    except Exception:
        msg = 'Token invalid/expired.'
        raise ValueError(msg)
    user = payload['username']

    return user


def closeConn(message):
    message.reply_channel.send({'close': True})

def jwt_authenticate(func):
    @wraps(func)
    def inner(message):
        try:
            if(message.channel_session['user']):
                return func(message)
        except Exception:
            params=parse_get(message.content['query_string'])
            token = params['token']
            if token is None:
                return closeConn(message)
            user = authenticate(token)
            message.channel_session['user'] = user
            try:
                message.channel_session['chatid']=params['chatId']
                message.channel_session['lastmsgid']=params['lastMsgId']
            except Exception:
                print("List")
            return func(message)
    return inner
