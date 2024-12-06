from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from debug_toolbar.toolbar import debug_toolbar_urls

from apps.generals.utils import health
from config import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/account/", include("apps.account.urls_v1")),
    path("api/v2/account/", include("apps.account.urls_v2")),
    path("api/v1/chat/", include("apps.chat.urls")),
    path("api/v1/health/", health),
] + debug_toolbar_urls()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
