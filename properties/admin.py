from django.contrib import admin
from django.utils.html import format_html
from .models import Property

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'status', 'created_at', 'created_by', 'image_preview')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'location', 'description')
    ordering = ('-created_at',)

    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" height="60" style="object-fit: cover; border-radius: 6px;" />', obj.image.url)
        return "—"
    
    image_preview.short_description = 'الصورة'
