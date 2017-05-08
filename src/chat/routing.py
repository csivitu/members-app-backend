# routing.py
from channels.routing import route

channel_routing = [
    route('websocket.connect', 'chat.consumers.chat_list',path=r"^/chat/list"),
    route('websocket.receive', 'chat.consumers.chat_message', path=r"^/chat/chat"),
    route('websocket.connect', 'chat.consumers.chat_connect', path=r"^/chat/chat"),
    route('websocket.disconnect','chat.consumers.chat_disconnect',path=r"^/chat/chat")
]
