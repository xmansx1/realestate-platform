from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # تسجيل حساب
    path('تسجيل/', views.signup, name='signup'),


    # الطلبات
    path('property/image/delete/<int:image_id>/', views.delete_property_image, name='delete_property_image'),
    path('طلب-عقار/', views.create_property_request, name='create_property_request'), 
    path('طلباتي/', views.my_requests, name='my_requests'),
    path('تعديل-طلب/<int:request_id>/', views.edit_request, name='edit_request'),
    path('حذف-طلب/<int:request_id>/', views.delete_request, name='delete_request'),
    path('طلبات-العقارات/', views.property_requests, name='property_requests'),
    path('لوحة-التحكم/إضافة-مستخدم/', views.add_user, name='add_user'),
    path('تعديل-طلب/<int:request_id>/', views.edit_request, name='edit_request'),
   path('طلبات-العقار/', views.property_requests, name='property_requests'),
   path('حذف-طلب/<int:request_id>/', views.delete_request, name='delete_request'),

    

    path('عقار/إضافة/', views.add_property, name='add_property'),
    path('عقاراتي/', views.my_properties, name='my_properties'),
    path('عقار/تعديل/<int:pk>/', views.edit_property, name='edit_property'),
    path('عقار/حذف/<int:pk>/', views.delete_property, name='delete_property'),
    path('طلباتي/', views.my_requests, name='my_requests'),
    # لوحة التحكم والتصدير
    path('لوحة-التحكم/', views.dashboard, name='dashboard'),
     path('عقار/<int:pk>/', views.property_detail, name='property_detail'),

    path('', views.home, name='home'),

    path('طلب-عقاري/<int:request_id>/', views.request_detail, name='request_detail'),

    path('تصدير-طلبات/', views.export_requests_excel, name='export_requests_excel'),
     path('تغيير-كلمة-المرور/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/change_password.html',
        success_url='/تغيير-كلمة-المرور/تم/',
    ), name='change_password'),

    path('تغيير-كلمة-المرور/تم/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'
    ), name='password_change_done'),
]
