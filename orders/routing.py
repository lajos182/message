from django.urls import re_path
from orders import consumers

websocket_urlpatterns = [
    re_path(r'^ws/order/(?P<service_uid>[^/]+)/$', consumers.OrderResult),
]