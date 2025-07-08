from django.urls import path
from . import views

app_name = 'ownership'

urlpatterns = [
    # ------------------------
    # 🔹 لوحة تحكم المالك
    # ------------------------
    path('dashboard/', views.owner_dashboard_view, name='owner_dashboard'),

    # ------------------------
    # 🔹 إدارة العقارات
    # ------------------------
    path('properties/', views.my_properties_view, name='my_properties'),
    path('properties/add/', views.add_property_view, name='add_property'),
    path('properties/<int:pk>/edit/', views.edit_property_view, name='edit_property'),
    path('properties/<int:pk>/', views.property_detail_view, name='property_detail'),
    path('properties/<int:pk>/delete/', views.delete_property_view, name='delete_property'),

    # ------------------------
    # 🔹 إدارة الوحدات
    # ------------------------
    path('properties/<int:pk>/units/', views.property_units_view, name='property_units'),
    path('properties/<int:pk>/units/add/', views.add_unit_view, name='add_unit'),
    path('units/<int:pk>/', views.unit_detail_view, name='unit_detail'),
    path('units/<int:pk>/edit/', views.edit_unit_view, name='edit_unit'),
    path('units/<int:pk>/delete/', views.delete_unit_view, name='delete_unit'),

    # ------------------------
    # 🔹 إدارة العقود والتحديثات
    # ------------------------
    path('units/<int:pk>/rental/add/', views.add_rental_contract_view, name='add_rental_contract'),
    path('units/<int:pk>/updates/add/', views.add_unit_update_view, name='add_unit_update'),
    path('units/<int:pk>/expenses/add/', views.add_unit_expense_view, name='add_unit_expense'),

    # ------------------------
    # 🔹 التقرير العام للمالك
    # ------------------------
    path('report/', views.owner_report_view, name='owner_report'),
]
