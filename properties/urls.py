from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    path('', views.property_list, name='list'),
    path('admin/', views.property_list, name='admin_list'),
    path('admin/create/', views.property_create, name='admin_create'),
    path('admin/<int:pk>/edit/', views.property_update, name='admin_edit'),
    path('admin/<int:pk>/delete/', views.property_delete, name='admin_delete'),
    path('view/<int:pk>/', views.property_detail, name='property_detail'),
    

]
