import stripe
from django.conf import settings
from django.urls import reverse
from django.views.generic import TemplateView
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework.permissions import AllowAny

from .filters import PaymentFilter
from .models import User, Payment
from .permissions import IsOwnerOrReadOnly
from .serializers import PaymentSerializer, UserSerializer, UserUpdateSerializer, UserProfileSerializer


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
        # Creating stripe.Product
        payment = serializer.save()

        stripe.api_key = settings.STRIPE_API_KEY

        stripe_product = stripe.Product.create(
            name=payment.course.name,
            description=payment.course.description
        )
        # Creating Stripe.Price
        stripe_price = stripe.Price.create(
            currency="usd",
            unit_amount=int(payment.course.amount * 100),
            product=stripe_product
        )
        # Creating stripe.Session
        session = stripe.checkout.Session.create(
            success_url=self.request.build_absolute_uri(reverse('users:successful-payment')),
            line_items=[
                {
                    "price": stripe_price,
                    "quantity": 1
                }
            ],
            mode="payment",
        )
        payment.link = session.url
        payment.session_id = session.id
        payment.save()


class SuccessPaymentView(TemplateView):
    template_name = 'success_payment.html'
