# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.utils.translation import gettext_lazy as _


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('full_name', 'phone', 'email', 'role', 'is_active')
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined',)

    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('معلومات شخصية', {'fields': ('full_name', 'email', 'city', 'district', 'val_license')}),
        ('الصلاحيات', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('تواريخ', {'fields': ('last_login', 'date_joined')}),  # date_joined فقط للعرض
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'full_name', 'email', 'city', 'district', 'val_license', 'role', 'password1', 'password2'),
        }),
    )
