from django.urls import include, path
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tag', TagViewSet)
router.register(r'likedis', LikeOrDislikeViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'', PostViewSet)

urlpatterns = [
    
]

urlpatterns += router.urls