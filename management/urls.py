from django.urls import path
from . import views

app_name = 'management'

urlpatterns = [
    # عقاراتي
    path('my-properties/', views.my_properties, name='my_properties'),
    path('add-property/', views.add_property, name='add_property'),
    path('my-properties/units/', views.owner_properties_units, name='owner_properties_units'),
    path('assign-staff/', views.assign_staff_view, name='assign_staff'),
    # مستندات العقار
    path('property/<int:property_id>/upload-documents/', views.upload_documents, name='upload_documents'),
    path('my-properties/<int:pk>/documents/', views.property_documents_view, name='property_documents'),
    path('my-properties/<int:pk>/documents/edit/', views.update_property_documents, name='edit_documents'),

    # الوحدات
    path('my-properties/<int:pk>/units/add/', views.add_unit_to_property, name='add_unit'),
    path('unit/<int:pk>/', views.unit_detail_view, name='unit_detail'),
    path('unit/<int:unit_id>/edit/', views.edit_unit, name='edit_unit'),
    path('unit/<int:pk>/delete/', views.delete_unit, name='delete_unit'),

    # عقود الإيجار
    path('unit/<int:unit_id>/rental/add/', views.add_rental_info, name='add_rental_info'),
    path('unit/<int:unit_id>/rental/edit/', views.edit_rental_info, name='edit_rental_info'),
    path('unit/<int:unit_id>/rental/delete/', views.delete_rental_info, name='delete_rental_info'),

    # تحديثات ومصروفات
    path('unit/<int:unit_id>/updates/', views.unit_updates_view, name='unit_updates'),
    path('unit/<int:unit_id>/updates/add/', views.add_unit_update, name='add_unit_update'),
    path('unit/update/<int:update_id>/edit/', views.edit_unit_update, name='edit_unit_update'),
    path('unit/update/<int:update_id>/delete/', views.delete_unit_update, name='delete_unit_update'),

    # الصيانة
    path('units/<int:unit_id>/maintenance/', views.unit_maintenance_list, name='unit_maintenance_list'),
    path('maintenance/edit/<int:pk>/', views.edit_scheduled_maintenance, name='edit_scheduled_maintenance'),
    path('maintenance/delete/<int:pk>/', views.delete_scheduled_maintenance, name='delete_scheduled_maintenance'),

    # المشرف: عرض العقارات ولوحة التعيين
    path('admin-properties/', views.admin_properties_view, name='admin_properties'),

    # ✅ هذا هو مسار الصفحة التي تعرض جدول التعيين
    path('assign-staff-view/', views.assign_staff_view, name='assign_staff_view'),

    # ✅ هذا هو المسار المستخدم في AJAX (POST)
    path('assign-staff/', views.assign_staff_to_unit, name='assign_staff'),
]
