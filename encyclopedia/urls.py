# encyclopedia/urls.py

from django.urls import path
from . import views  # Import widoków z tej aplikacji

urlpatterns = [
    # Strona główna - wyświetla dostępne wpisy
    path("", views.index, name="index"),  # URL: /

    # Strona do tworzenia nowego wpisu
    path("create/", views.create, name="create"),  # URL: /create/

    # Losowy wpis - wyświetla losowy wpis
    path("random/", views.random_entry, name="random"),  # URL: /random/

    # Strona wyszukiwania
    path("search/", views.search, name="search"),  # URL: /search/

    # Pojedynczy wpis (np. HTML, CSS, Django)
    path("wiki/<str:title>/", views.entry, name="entry"),  # URL: /wiki/<title>/

    # Edytowanie konkretnego wpisu
    path("wiki/<str:title>/edit/", views.edit_entry, name="edit_entry"),  # URL: /wiki/<title>/edit/
]
