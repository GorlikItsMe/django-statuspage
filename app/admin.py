from django.contrib import admin
from .models import Service, ServiceCheck


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'pos', 'name', 'status', 'interval', 'timeout', 'pos', 'url', 'check_method')
    search_fields = ('id', 'name', 'desc', 'link', 'check_method', 'url')
    ordering = ['pos']

    fieldsets = (
        ('General', {
            'fields': ('name', 'desc', 'link', 'pos', 'status')
        }),
        ('Checking status settings', {
            # 'classes': ('collapse',),
            'fields': ('check_method', 'interval', 'timeout', 'url'),
        }),
    )


@admin.register(ServiceCheck)
class ServiceCheckAdmin(admin.ModelAdmin):
    list_display = ('id', 'datetime', 'service', 'latency', 'online')
    search_fields = ('id', 'datetime', 'service__name', 'latency', 'online')
