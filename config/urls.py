from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from pages.views import landing

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", landing, name="home"),
    path("accounts/", include("accounts.urls")),
    path("colleges/", include("colleges.urls")),
    path("documents/", include("catalog.urls")),
    path("applications/", include("applications.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
