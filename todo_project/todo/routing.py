from django.urls import path

from todo.consumers import TodoConsumer

websocket_urlpatterns = [
    path("ws/todo/", TodoConsumer.as_asgi()),
]