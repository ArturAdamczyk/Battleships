# routing.py
from channels import route

channel_routing = [
    route('websocket.connect', 'battleships.consumers.ws_add',
          path=r'^/game/(?P<game>\w+)$'),
]