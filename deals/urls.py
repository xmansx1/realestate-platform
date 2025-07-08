# deals/urls.py
from django.urls import path
from . import views
from .views import create_deal_view

app_name = 'deals'

urlpatterns = [
    path('admin/list/', views.admin_deals_view, name='admin_deals'),
    path('agent/list/', views.agent_deals_view, name='agent_deals'),
    path('create/<int:request_id>/', create_deal_view, name='create_deal'),
]
