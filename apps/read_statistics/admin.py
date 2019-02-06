from django.contrib import admin
from .models import ReadTimes, ReadDetail


@admin.register(ReadTimes)
class ReadTimeAdmin(admin.ModelAdmin):
	list_display = ('id', 'read_times', 'content_type')


@admin.register(ReadDetail)
class ReadDetailAdmin(admin.ModelAdmin):
	list_display = ('id', 'date', 'read_number', 'content_type')

