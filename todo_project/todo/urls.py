# urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import TodoViewSet, websocket

router = DefaultRouter()
router.register(r'todo', TodoViewSet, basename='todo')

urlpatterns = router.urls


urlpatterns += [
    path('websocket', websocket, name='websocket'),
]
