from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from .models import User

# Register your models here.

UserAdmin.fieldsets[2][1]['fields'] = (
    'is_active',
    'is_staff',
    'is_superuser',
    'groups',
    'user_permissions',
    'author',
    'special_user',
    )
UserAdmin.list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'author', 'is_special_user')



admin.site.register(User, UserAdmin)