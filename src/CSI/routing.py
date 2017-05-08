from channels.routing import route, include

from chat.routing import channel_routing


routing = [
    include(channel_routing, path=r"^/chat"),
]