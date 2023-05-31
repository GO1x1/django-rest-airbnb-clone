from django.urls import path
from rest_framework import routers

from users.views import UsersViewSet

app_name = "users"

router = routers.DefaultRouter()
router.register('', UsersViewSet)

urlpatterns = router.urls
