from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    ordering = ('email', 'first_name', 'last_name', 'phone_number', 'role',
                'is_staff', 'is_superuser',)
    list_filter = ('email', 'first_name', 'last_name', 'phone_number', 'role',
                'is_staff', 'is_superuser',)
    list_display = ['email', 'first_name', 'last_name',
            'phone_number', 'role',
            'is_staff', 'is_superuser', 'date_created', 'date_updated']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name',
                                    'phone_number', 'date_created',
                                    'date_updated')}),
        ('Permissions', {'fields': ('is_staff', 'role')}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name',
                                    'phone_number')}),
        ('Permissions', {'fields': ('is_staff', 'role')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
