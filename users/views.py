from django.urls import reverse
from django.views.generic import TemplateView
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework.permissions import AllowAny

from .filters import PaymentFilter
from .models import User, Payment
from .permissions import IsOwnerOrReadOnly
from .serializers import PaymentSerializer, UserSerializer, UserUpdateSerializer, UserProfileSerializer
from .services import StripeService


class PaymentListView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [SearchFilter, OrderingFilter, filters.DjangoFilterBackend]
    filterset_class = PaymentFilter
    search_fields = ['course__name', 'lesson__title', 'method']
    ordering_fields = ['date']


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserProfileSerializer

class PaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):

        if not self.request.user.is_authenticated:
            raise PermissionDenied("You must be logged in to create a payment.")
        serializer.validated_data['user'] = self.request.user

        payment = serializer.save()

        if payment.method == 'CRD':
            stripe_service = StripeService()
            success_url = self.request.build_absolute_uri(reverse('users:successful-payment'))
            stripe_service.handle_payment(payment, success_url)
        elif payment.method == 'CSH':
            payment.status = 'success'
            payment.save()
        else:
            raise ValueError(f'Invalid payment method: {payment.method}')



class SuccessPaymentView(TemplateView):
    template_name = 'success_payment.html'
