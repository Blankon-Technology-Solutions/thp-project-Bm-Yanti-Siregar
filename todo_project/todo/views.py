from rest_framework import permissions
from drf_rw_serializers import viewsets

from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render

from .models import Todo
from .serializers import TodoSerializer, TodoDeserializer
from .filters import TodoFilter


class TodoViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated] 
    filter_backends = [DjangoFilterBackend]
    filterset_class = TodoFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TodoSerializer
        return TodoDeserializer

    def get_queryset(self):
        # Retrieve todos associated with the current user
        return Todo.objects.filter(user=self.request.user)


def websocket(request):
    return render(request, 'websocket.html')

