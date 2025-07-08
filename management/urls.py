from django.urls import path
from . import views

app_name = 'management'

urlpatterns = [
    # ------------------------
    # 🔹 إدارة العقارات (للمالك)
    # ------------------------
    path('my-properties/', views.my_properties, name='my_properties'),
    path('add-property/', views.add_property, name='add_property'),
    path('my-properties/units/', views.owner_properties_units, name='owner_properties_units'),
    path('my-properties/<int:pk>/edit/', views.edit_property, name='edit_property'),
    path('my-properties/<int:pk>/units/', views.property_units_view, name='property_units'),
    # ------------------------
    # 🔹 مستندات العقار
    # ------------------------
    path('property/<int:pk>/upload-documents/', views.upload_documents, name='upload_documents'),
    path('my-properties/<int:pk>/documents/', views.property_documents_view, name='property_documents'),
    path('my-properties/<int:pk>/documents/edit/', views.update_property_documents, name='edit_documents'),

    # ------------------------
    # 🔹 الوحدات
    # ------------------------
    path('my-properties/<int:pk>/units/add/', views.add_unit_to_property, name='add_unit'),
    path('unit/<int:pk>/', views.unit_detail_view, name='unit_detail'),
    path('unit/<int:pk>/edit/', views.edit_unit, name='edit_unit'),
    path('unit/<int:pk>/delete/', views.delete_unit, name='delete_unit'),

    # ------------------------
    # 🔹 عقود الإيجار
    # ------------------------
    path('unit/<int:pk>/rental/add/', views.add_rental_info, name='add_rental_info'),
    path('unit/<int:pk>/rental/edit/', views.edit_rental_info, name='edit_rental_info'),
    path('unit/<int:pk>/rental/delete/', views.delete_rental_info, name='delete_rental_info'),

    # ------------------------
    # 🔹 تحديثات ومصروفات
    # ------------------------
    path('unit/<int:pk>/updates/', views.unit_updates_view, name='unit_updates'),
    path('unit/<int:pk>/updates/add/', views.add_unit_update, name='add_unit_update'),
    path('unit/update/<int:pk>/edit/', views.edit_unit_update, name='edit_unit_update'),
    path('unit/update/<int:pk>/delete/', views.delete_unit_update, name='delete_unit_update'),

    # ------------------------
    # 🔹 الصيانة المجدولة
    # ------------------------
    path('unit/<int:pk>/maintenance/', views.unit_maintenance_list, name='unit_maintenance_list'),
    path('maintenance/edit/<int:pk>/', views.edit_scheduled_maintenance, name='edit_scheduled_maintenance'),
    path('maintenance/delete/<int:pk>/', views.delete_scheduled_maintenance, name='delete_scheduled_maintenance'),

    # ------------------------
    # 🔹 للمشرفين: إدارة العقارات وتعيين الموظفين
    # ------------------------
    path('admin-properties/', views.admin_properties_view, name='admin_properties'),
    path('assign-staff-view/', views.assign_staff_view, name='assign_staff_view'),
    
    path('assign-staff/ajax/', views.assign_staff, name='assign_staff_ajax'),

]
