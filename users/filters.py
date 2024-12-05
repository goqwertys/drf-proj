from django_filters import rest_framework as filters
from .models import Payment

class PaymentFilter(filters.FilterSet):
    date = filters.OrderingFilter(fields=['date'])
    course = filters.CharFilter(field_name='course__name', lookup_expr='icontains')
    lesson = filters.CharFilter(field_name='lesson__title', lookup_expr='icontains')
    method = filters.CharFilter(field_name='method', lookup_expr='exact')

    class Meta:
        model = Payment
        fields = ['course', 'lesson', 'method']