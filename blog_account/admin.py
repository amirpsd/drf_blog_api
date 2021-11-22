from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.

UserAdmin.fieldsets[2][1]['fields'] = (
    'is_active',
    'is_staff',
    'is_superuser',
    'groups',
    'user_permissions',
    'author',
    )
UserAdmin.list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'author')



admin.site.register(User, UserAdmin)