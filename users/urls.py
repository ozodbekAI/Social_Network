from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import *



router = DefaultRouter()
router.register('user', UserViewSet, basename="user")
router.register('friends', FriednShip, basename="firends")


urlpatterns = [
    
    path('', include(router.urls))
]