from django.contrib import admin
from .models import Deal

@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ('id', 'request', 'executed_by', 'commission', 'platform_share', 'created_at')
    list_filter = ['created_at']
    search_fields = ['request__id', 'executed_by__full_name']
