from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from core import models

class UserAdmin(BaseUserAdmin):
    """Admin page for User model"""
    list_display = ['username', 'first_name', 'last_name', 'is_staff']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)})
    )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(models.Question)
