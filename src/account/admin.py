from django.contrib import admin

from .models import User

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "phone", "first_name",
        "last_name", "is_staff",
        "author", "is_special_user",
    )
    list_filter = (
        "is_staff", "is_superuser", 
        "groups",
    )
    search_fields = (
        "first_name", "last_name", 
        "phone",
    )
    ordering = (
        "-is_superuser", "-is_staff", 
        "-pk",
    )
    list_per_page = 25


