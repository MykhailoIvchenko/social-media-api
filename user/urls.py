from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, UserFollowViewSet

router = DefaultRouter()
router.register(r'profile', UserProfileViewSet, basename='user-profile')
router.register(r'follow', UserFollowViewSet, basename='user-follow')

urlpatterns = [
    path('', include(router.urls)),
]
