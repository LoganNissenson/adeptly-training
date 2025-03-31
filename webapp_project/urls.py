"""webapp_project URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Import the debug view and health check
from debug_view import debug_info
from health_check import health_check
from adeptly.simple_views import simple_home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('adeptly.urls')),
    path('debug/', debug_info),  # Add a debug URL
    path('health/', health_check),  # Add a health check URL
    path('test/', simple_home),  # Add a simple test page
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
