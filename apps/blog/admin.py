from django.contrib import admin
from .models import Blog, BlogCategory


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
	list_display = ("id", "type_name")


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
	list_display = ("id", "type_name", "title", "get_read_times", "create_time", "last_updated_time")
