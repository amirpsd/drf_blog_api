from django.contrib import admin
from .models import Comment
# Register your models here.

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'create', 'rate')
    list_per_page = 30

