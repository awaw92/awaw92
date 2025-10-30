# wiki/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Ścieżka do panelu administracyjnego Django
    path('admin/', admin.site.urls),  # dostęp do panelu admin pod /admin

    # Ścieżka do aplikacji 'encyclopedia'
    # Wszystkie URL-e w 'encyclopedia/urls.py' będą dostępne pod głównym adresem
    path('', include('encyclopedia.urls')),  # obsługuje URL-e w aplikacji 'encyclopedia'
]
