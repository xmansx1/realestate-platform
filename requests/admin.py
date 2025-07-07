from django.contrib import admin
from .models import RealEstateRequest

@admin.register(RealEstateRequest)
class RealEstateRequestAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone_number', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['full_name', 'phone_number', 'property__title']
