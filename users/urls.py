from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, UserRegistrationView

router = DefaultRouter()
router.register('profile', UserProfileViewSet, basename='profile')

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('', include(router.urls)),
]
