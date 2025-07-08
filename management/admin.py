from django.contrib import admin
from .models import (
    Property,
    Unit,
    RentalContract,
    UpdateLog,
    PropertyDocument,
    ScheduledMaintenance
)

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city', 'district', 'owner', 'is_approved')
    list_filter = ('city', 'is_approved')
    search_fields = ('name', 'city', 'district', 'owner__username')
    raw_id_fields = ('owner',)

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('id', 'unit_number', 'property', 'status', 'area', 'price', 'assigned_to')
    list_filter = ('status', 'property__city')
    search_fields = ('unit_number', 'property__name')
    raw_id_fields = ('property', 'assigned_to')

@admin.register(RentalContract)
class RentalContractAdmin(admin.ModelAdmin):
    list_display = ('id', 'unit', 'tenant_name', 'start_date', 'end_date', 'amount', 'payment_method')
    list_filter = ('payment_method', 'start_date', 'end_date')
    search_fields = ('tenant_name', 'unit__unit_number')
    raw_id_fields = ('unit',)

@admin.register(UpdateLog)
class UpdateLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'unit', 'update_type', 'date', 'amount')
    list_filter = ('update_type', 'date')
    search_fields = ('unit__unit_number', 'update_type')
    raw_id_fields = ('unit',)

@admin.register(PropertyDocument)
class PropertyDocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'property', 'description', 'uploaded_by', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('property__name', 'description')
    raw_id_fields = ('property', 'uploaded_by')

@admin.register(ScheduledMaintenance)
class ScheduledMaintenanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'unit', 'maintenance_type', 'scheduled_date', 'created_at')
    list_filter = ('scheduled_date',)
    search_fields = ('unit__unit_number', 'maintenance_type')
    raw_id_fields = ('unit',)
