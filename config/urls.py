from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from core.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('accounts/', include('accounts.urls')),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('requests/', include('requests.urls')),
    path('owner/', include('ownership.urls')),
    # ✅ مرة واحدة فقط لكل namespace
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('properties/', include(('properties.urls', 'properties'), namespace='properties')),
    path('requests/', include(('requests.urls', 'requests'), namespace='requests')),
    path('notifications/', include(('notifications.urls', 'notifications'), namespace='notifications')),
    path('dashboard/', include(('dashboard.urls', 'dashboard'), namespace='dashboard')),
    path('deals/', include(('deals.urls', 'deals'), namespace='deals')),
    path('management/', include(('management.urls', 'management'), namespace='management')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
