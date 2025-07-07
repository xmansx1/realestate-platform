from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from core.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),

    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('properties/', include(('properties.urls', 'properties'), namespace='properties')),
    path('requests/', include(('requests.urls', 'requests'), namespace='requests')),
    path('notifications/', include(('notifications.urls', 'notifications'), namespace='notifications')),
    path('dashboard/', include(('dashboard.urls', 'dashboard'), namespace='dashboard')),
    path('notifications/', include('notifications.urls', namespace='notifications')),
    path('admin/dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('requests/', include('requests.urls')),
    path('requests/', include('requests.urls', namespace='requests')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
