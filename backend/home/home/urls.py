# your_project/urls.py (main project urls.py)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/', include('app.urls')),  # Replace 'your_app' with your actual app name
]

# CRITICAL: Add this to serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Also serve static files if needed
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)