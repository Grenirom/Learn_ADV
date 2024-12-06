from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.chat.views import RoomViewSet, MessageViewSet

router = DefaultRouter()
router.register("rooms", RoomViewSet)
router.register("messages", MessageViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
