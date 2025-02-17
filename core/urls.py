from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

handler404 = 'videos.views.page_not_found'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('videos.urls')),
    path('account/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
