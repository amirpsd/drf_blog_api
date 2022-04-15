from django.contrib import admin

from .models import Blog, Category

# Register your models here.

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'slug', 
        'author', 'special', 
        'status', 'visits',
    )
    search_fields = (
        'title', 'author__first_name', 
        'category__title',
    )
    list_filter = (
        'status', 'special', 
        'publish',
    )
    exclude = (
        "slug",
    )
    filter_horizontal = (
        "category", "likes",
    )
    radio_fields = {
        "status": admin.HORIZONTAL
    }
    list_per_page = 25


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'slug', 
        'parent', 'status',
    )
    search_fields = (
        'title', 'slug', 
        'status',
    )
    list_filter = (
        ['status']
    )
    list_per_page = 25