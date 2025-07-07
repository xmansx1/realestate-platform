from django.contrib import admin
from .models import Property, Unit, RentalInfo, UpdateLog


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city', 'district', 'owner', 'is_approved')
    list_filter = ('is_approved', 'city', 'district')
    search_fields = ('name', 'owner__full_name')
    raw_id_fields = ('owner',)


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('id', 'unit_number', 'property', 'status', 'area', 'price', 'assigned_to')
    list_filter = ('status', 'property__city')
    search_fields = ('unit_number', 'property__name')
    raw_id_fields = ('property', 'assigned_to')


@admin.register(RentalInfo)
class RentalInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'unit', 'tenant_name', 'start_date', 'end_date', 'amount')
    list_filter = ('start_date', 'end_date')
    search_fields = ('tenant_name', 'unit__unit_number')
    raw_id_fields = ('unit',)


@admin.register(UpdateLog)
class UpdateLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'unit', 'update_type', 'date', 'amount')
    list_filter = ('update_type', 'date')
    search_fields = ('unit__unit_number', 'update_type')
    raw_id_fields = ('unit',)
