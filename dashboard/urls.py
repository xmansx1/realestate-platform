from django.urls import path
from .views import dashboard_view
from .views import admin_dashboard_view
from .views import admin_dashboard_view, export_deals_excel

app_name = 'dashboard'

urlpatterns = [
    path('', dashboard_view, name='home'),
    path('', admin_dashboard_view, name='admin_dashboard'),
    path('export-excel/', export_deals_excel, name='export_excel'),
]
