from django.urls import path, include
from rest_framework import routers

from rooms.views import RoomViewSet

app_name = "rooms"

router = routers.DefaultRouter()
router.register('', RoomViewSet)

urlpatterns = router.urls