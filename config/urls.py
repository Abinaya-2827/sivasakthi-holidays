from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("accounts/", include("accounts.urls")),
    path("destinations/", include("destinations.urls")),
    path("packages/", include("packages.urls")),
    path("gallery/", include("gallery.urls")),
]

# Media (uploaded destination/gallery/hero photos) is served by Django
# itself even when DEBUG=False. This isn't ideal at large scale (a real
# CDN/object-storage backend like S3 would be better), but it's what
# makes uploaded images actually load on a small single-server deploy
# instead of 404ing the moment DEBUG is turned off.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / "static")
