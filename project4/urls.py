from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("network.urls")),
]

# Obsługuje pliki statyczne w trybie debug
if settings.DEBUG:
    # Dodajemy obsługę plików statycznych z folderu 'network/static'
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
