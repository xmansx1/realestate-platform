from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.unified_login_view, name='login'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage-users/', views.manage_users, name='manage_users'),
    # إدارة المستخدمين
    path('users/', views.user_list_view, name='user_list'),
    path('users/add/', views.user_create_view, name='user_create'),
    path('users/<int:user_id>/edit/', views.user_edit_view, name='user_edit'),
    path('users/<int:user_id>/toggle/', views.toggle_user_status, name='toggle_user_status'),
    path('users/<int:user_id>/delete/', views.user_delete_view, name='user_delete'),
]
