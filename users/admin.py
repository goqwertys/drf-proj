from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone_number', 'city', 'avatar', )
    list_filter = ('is_staff', 'is_active', 'city',)
    search_fields = ('email', 'phone_number', 'city',)
    ordering = ('id',)
