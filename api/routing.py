from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/SNreadings/',consumers.SMReadingsConsumer.as_asgi()),
    re_path(r'ws/SKreadings/',consumers.SKReadingsConsumer.as_asgi())
]