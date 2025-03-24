from django.contrib import admin
from .models import Property, PropertyRequest, PropertyImage

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'city', 'property_type', 'request_type', 'created_at')
    search_fields = ('full_name', 'city', 'district', 'property_type')
    list_filter = ('city', 'request_type', 'property_type')

@admin.register(PropertyRequest)
class PropertyRequestAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'property_type', 'request_type', 'city', 'created_at')
    search_fields = ('full_name', 'city', 'district')
    list_filter = ('request_type', 'property_type')

@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('property', 'image')

from django.contrib import admin
from .models import News

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['title']

from .models import FooterSettings

@admin.register(FooterSettings)
class FooterSettingsAdmin(admin.ModelAdmin):
    list_display = ['about', 'whatsapp', 'phone']
    

    from django.contrib import admin
from django.contrib.admin.sites import AdminSite

class MyAdminSite(AdminSite):
    site_header = "لوحة إدارة منصة العقارات"
    site_title = "منصة العقارات"
    index_title = "التحكم في المحتوى"

    def each_context(self, request):
        context = super().each_context(request)
        context['css_files'] = ['/static/css/admin-arabic.css']
        return context

admin_site = MyAdminSite(name='myadmin')
