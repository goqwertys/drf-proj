from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .apps import UsersConfig
from .views import PaymentListView, UserCreateAPIView, UserProfileViewSet, PaymentCreateAPIView, SuccessPaymentView

app_name = UsersConfig.name

router = SimpleRouter()
router.register('profiles', UserProfileViewSet)

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='refresh'),

    path('payments/', PaymentListView.as_view(), name='payment-list'),
    path('payments/create/', PaymentCreateAPIView.as_view(), name='payment-create'),

    path('payments/success/', SuccessPaymentView.as_view(), name='successful-payment')
]

urlpatterns += router.urls
