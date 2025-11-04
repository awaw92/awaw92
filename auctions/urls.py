from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = "auctions"

urlpatterns = [
    # Strona główna - lista aktywnych aukcji
    path("", views.index, name="index"),

    # Logowanie i wylogowanie użytkownika
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Rejestracja nowego użytkownika
    path("register/", views.register, name="register"),

    # Tworzenie nowej aukcji (tylko dla zalogowanych użytkowników)
    path("create/", login_required(views.create_listing), name="create_listing"),

    # Szczegóły pojedynczej aukcji (obsługa ofert i komentarzy)
    path("listing/<int:listing_id>/", views.listing_detail, name="listing_detail"),

    # Edytowanie aukcji (tylko dla autora aukcji)
    path("listing/<int:listing_id>/edit/", login_required(views.edit_listing), name="edit_listing"),

    # Usuwanie aukcji (tylko dla autora aukcji)
    path("listing/<int:listing_id>/delete/", login_required(views.delete_listing), name="delete_listing"),

    # Profil użytkownika
    path("profile/", login_required(views.user_profile), name="user_profile"),

    # Watchlist
    path("watchlist/", login_required(views.view_watchlist), name="view_watchlist"),
    path("listing/<int:listing_id>/add_to_watchlist/", login_required(views.add_to_watchlist), name="add_to_watchlist"),
    path("listing/<int:listing_id>/remove_from_watchlist/", login_required(views.remove_from_watchlist), name="remove_from_watchlist"),

    # Kategorie
    path("categories/", views.category_list, name="category_list"),  # Wyświetlanie wszystkich kategorii
    path("category/<int:category_id>/", views.category_detail, name="category_detail"),  # Aukcje w konkretnej kategorii
]
