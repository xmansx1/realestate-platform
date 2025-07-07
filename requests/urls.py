from django.urls import path
from . import views
from .views import (
    my_reserved_requests,
    execute_request,
    available_requests_for_agent,
    reserve_request,
    # أي دوال أخرى مستخدمة في urls
)
from .views import my_deals_view

app_name = 'requests'

urlpatterns = [
    path('admin/', views.admin_request_list, name='admin_list'),
    path('admin/<int:pk>/', views.admin_request_detail, name='admin_detail'),
    path('create/<int:property_id>/', views.create_request, name='create'),
    path('general-request/', views.create_general_request, name='general_request'),
    path('admin/<int:pk>/mark-reviewed/', views.mark_request_as_reviewed, name='mark_reviewed'),
    path('admin/<int:pk>/mark-contacted/', views.mark_request_as_contacted, name='mark_contacted'),
    path('mark-reviewed/<int:pk>/', views.mark_reviewed, name='mark_reviewed'),
    path('mark-contacted/<int:pk>/', views.mark_contacted, name='mark_contacted'),
    path('admin/<int:pk>/delete/', views.admin_request_delete, name='admin_delete'),
    path('agent/available/', available_requests_for_agent, name='agent_available'),
    path('agent/reserve/<int:pk>/', reserve_request, name='agent_reserve'),
    path('agent/my-requests/', my_reserved_requests, name='agent_my_requests'),
    path('agent/execute/<int:pk>/', execute_request, name='agent_execute_request'),
    path('agent/my-deals/', my_deals_view, name='agent_my_deals'),
    path('requests/<int:request_id>/reserve/', views.reserve_request, name='reserve_request'),
    path('<int:request_id>/reserve/', views.reserve_request, name='reserve_request'),
    path('', views.request_list, name='requests:list'),
    path('', views.request_list, name='list')

]
