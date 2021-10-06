from django.contrib import admin

from .models import Category

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title','slug','parent','status')
    search_fields = ('title','slug','status')
    list_filter = (['status'])
    list_per_page = 30