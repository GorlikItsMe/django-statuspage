from django.contrib import admin
from .models import Service


@admin.register(Service)
class ServiceHttpAdmin(admin.ModelAdmin):
    list_display = ('id', 'pos', 'name', 'status', 'interval', 'timeout', 'pos', 'url', 'check_method')
    search_fields = ('id', 'name', 'desc', 'link', 'check_method', 'url')
    ordering = ['pos']

    fieldsets = (
        ('General', {
            'fields': ('name', 'desc', 'link', 'pos')
        }),
        ('Checking status settings', {
            # 'classes': ('collapse',),
            'fields': ('check_method', 'interval', 'timeout', 'url'),
        }),
    )
