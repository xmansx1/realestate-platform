from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # تسجيل الدخول والخروج
    path('تسجيل-دخول/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('تسجيل-خروج/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),  # هذا هو المهم ✅
    # روابط التطبيق الرئيسي
    path('', include('properties.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)