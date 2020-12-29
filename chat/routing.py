from django.urls import path
from chat.consumers import *

channel_routing = [
      path('chats/<str:user>/<int:room>/', ChatConsumerA.as_asgi()),
      path('',ChatConsumerB.as_asgi()),
]