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
