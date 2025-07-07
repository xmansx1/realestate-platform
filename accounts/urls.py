# accounts/urls.py

app_name = 'accounts'
from .views import admin_dashboard_view

from . import views
from django.urls import path
from .views import (
    admin_login_view, admin_logout_view, admin_dashboard_view,
    user_list_view, user_create_view, user_edit_view, toggle_user_status
)

app_name = 'accounts'

urlpatterns = [
    path('login/', admin_login_view, name='admin_login'),
    path('dashboard/', admin_dashboard_view, name='admin_dashboard'),
    path('logout/', admin_logout_view, name='admin_logout'),
    path('users/', user_list_view, name='user_list'),
    path('users/add/', user_create_view, name='user_create'),
    path('users/<int:user_id>/edit/', user_edit_view, name='user_edit'),
    path('users/<int:user_id>/toggle/', toggle_user_status, name='toggle_user_status'),
    path('users/<int:user_id>/delete/', views.user_delete_view, name='user_delete'),
    path('login/', views.login_view, name='login'),
    path('admin/dashboard/', admin_dashboard_view, name='admin_dashboard'),

]

