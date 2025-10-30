from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),                   # Strona główna
    path("create/", views.create, name="create"),          # Strona tworzenia nowej strony
    path("random/", views.random_entry, name="random"),    # Losowa strona
    path("search/", views.search, name="search"),          # Strona wyszukiwania
    path("wiki/<str:title>/", views.entry, name="entry"),  # Pojedynczy wpis
    path("wiki/<str:title>/edit/", views.edit_entry, name="edit_entry"),  # Edycja wpisu
]
