from datetime import timedelta

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
import orders.routing

from orders import consumers

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            orders.routing.websocket_urlpatterns
        )
    ),
    'channel': ChannelNameRouter({
        'service-detection': consumers.OrderResult,
        #  新增router
        'testing-print': consumers.BeatServer
    })
})