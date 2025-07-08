from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

from .views import (
    # إدارة المشرف
    admin_request_list, admin_request_detail, mark_request_as_reviewed, mark_request_as_contacted,
    admin_request_delete, admin_approve_request, approve_request,

    # الطلبات
    create_request, create_general_request,

    # الوسيط العقاري
    agent_dashboard_view, agent_add_property, available_requests_view, reserve_request,
    confirm_reserve_request, my_reserved_requests, cancel_reservation, execute_request,
    execute_deal, my_deals_view, agent_reserved_requests_view,

    # الزائر / القائمة العامة
    broker_request_list,
)

app_name = 'requests'

urlpatterns = [
    # ✅ روابط المشرف
    path('admin/', admin_request_list, name='admin_list'),
    path('admin/<int:pk>/', admin_request_detail, name='admin_detail'),
    path('admin/<int:pk>/mark-reviewed/', mark_request_as_reviewed, name='mark_reviewed'),
    path('admin/<int:pk>/mark-contacted/', mark_request_as_contacted, name='mark_contacted'),
    path('admin/<int:pk>/delete/', admin_request_delete, name='admin_delete'),
    path('admin/requests/<int:pk>/approve/', admin_approve_request, name='admin_approve'),
    path('admin/approve/<int:request_id>/', approve_request, name='approve_request'),

    # ✅ روابط إنشاء الطلبات
    path('create/<int:property_id>/', create_request, name='create'),
    path('general-request/', create_general_request, name='general_request'),

    # ✅ روابط الوسيط العقاري
    path('agent/dashboard/', agent_dashboard_view, name='agent_dashboard'),
    path('agent/add-property/', agent_add_property, name='agent_add_property'),
    path('agent/available/', available_requests_view, name='available_requests'),
    path('agent/reserved/', agent_reserved_requests_view, name='reserved_requests'),
    path('agent/confirm-reserve/<int:request_id>/', confirm_reserve_request, name='confirm_reserve'),
    path('agent/reserve/<int:pk>/', reserve_request, name='agent_reserve'),
    path('agent/my-requests/', my_reserved_requests, name='agent_reserved'),
    path('agent/my-deals/', my_deals_view, name='agent_deals'),
    path('agent/execute/<int:request_id>/', execute_deal, name='execute_deal'),
    path('agent/cancel-reservation/<int:request_id>/', cancel_reservation, name='cancel_reservation'),
    path('agent/dashboard/', views.agent_dashboard_view, name='agent_dashboard'),


    # ✅ روابط عامة (للطلبات)
    path('<int:request_id>/reserve/', reserve_request, name='reserve_request'),
    path('<int:request_id>/execute/', execute_request, name='execute_request'),
    path('<int:request_id>/cancel/', cancel_reservation, name='cancel_reservation'),

    # ✅ تسجيل الخروج
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('agent/available/', views.available_requests_view, name='agent_available'),
    
    # ✅ الصفحة الافتراضية
    path('', broker_request_list, name='list'),
]
