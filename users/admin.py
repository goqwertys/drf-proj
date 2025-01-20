from django.contrib import admin

from users.models import User, Payment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone_number', 'city', 'avatar', )
    list_filter = ('is_staff', 'is_active', 'city',)
    search_fields = ('email', 'phone_number', 'city',)
    ordering = ('id',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'date',
        'amount',
        'method',
        'status',
        'course',
        'lesson'
    )
    list_filter = (
        'method',
        'status',
        'date'
    )
    search_fields = (
        'user__email',
        'course__title',
        'lesson__title',
        'session_id'
    )
    ordering = ('-date',)
