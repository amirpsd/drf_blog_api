from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from .models import User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('phone', 'first_name', 'last_name', 'is_staff', "author", "is_special_user")
    list_filter = ('is_staff', 'is_superuser', 'groups')
    search_fields = ('first_name', 'last_name', 'phone')
    ordering = ('phone',)


admin.site.register(User, UserAdmin)