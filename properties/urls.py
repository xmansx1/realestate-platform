from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    # 👁️ عرض العقارات للزوار
    path('', views.property_list_view, name='list'),
    path('view/<int:pk>/', views.property_detail, name='property_detail'),
    path('<int:pk>/', views.property_detail, name='detail'),

    # 📋 لوحة المشرف - إدارة العقارات
    path('admin/', views.admin_property_list, name='admin_list'),
    path('admin/properties/', views.admin_property_list, name='admin_property_list'),
    path('admin/properties/create/', views.admin_create_property, name='admin_create'),
    path('admin/properties/edit/<int:pk>/', views.admin_edit_property, name='admin_edit'),
    path('admin/properties/delete/<int:pk>/', views.admin_delete_property, name='admin_delete'),
    path('admin/', views.admin_list, name='admin_list'), 
    # ✅ إدارة اعتماد العقارات
    path('admin/properties/approve/<int:pk>/', views.admin_approve_property, name='admin_approve_property'),
    path('admin/properties/unapprove/<int:pk>/', views.admin_unapprove_property, name='admin_unapprove_property'),
    path('property/<int:pk>/', views.property_detail, name='detail'),
]
