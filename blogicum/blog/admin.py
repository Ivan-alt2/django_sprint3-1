from django.contrib import admin
from .models import Category, Post, Location


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'created_at')
    search_fields = ('name', 'city')
    list_filter = ('city',)
    list_display_links = ('name',)
    empty_value_display = 'Не задано'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'pub_date',
        'location',
        'category',
        'is_published',
        'created_at'
    )
    list_editable = (
        'category',
    )
    search_fields = ('title', 'text')
    list_filter = ('category', 'author', 'is_published', 'location')
    list_display_links = ('title',)
    empty_value_display = 'Не задано'
    date_hierarchy = 'pub_date'
    ordering = ('-pub_date',)
