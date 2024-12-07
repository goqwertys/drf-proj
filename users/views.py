from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, CreateAPIView
from django_filters import rest_framework as filters
from rest_framework import serializers

from .filters import PaymentFilter
from .models import User, Payment
from .serializers import PaymentSerializer, UserSerializer


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