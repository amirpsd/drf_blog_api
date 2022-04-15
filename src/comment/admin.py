from django.contrib import admin

from .models import Comment

# Register your models here.

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'name', 
        'create', 'updated', 
        'body',
    )
    list_filter = (
        "create",
    )
    search_fields = (
        "name", "body",
    )
    list_per_page = 25

