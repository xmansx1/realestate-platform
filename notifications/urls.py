from django.urls import path
from . import views

app_name = "notifications"  # هذا مهم!

urlpatterns = [
    path('', views.notification_list, name='notification_list'),  # ← لاحظ الاسم هنا
    path('read/<int:pk>/', views.mark_notification_read, name='mark_notification_read'),
    path('mark-all-read/', views.mark_all_read, name='mark_all_read'),
]
