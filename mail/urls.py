from django.urls import path
from . import views

urlpatterns = [
    # Strony HTML
    path("", views.index, name="index"),  # Strona główna
    path("login/", views.login_view, name="login"),  # Logowanie
    path("logout/", views.logout_view, name="logout"),  # Wylogowanie
    path("register/", views.register, name="register"),  # Rejestracja

    # Widok startowy mailbox w HTML
    path("mailbox/", views.mailbox_home, name="mailbox-home"),  # NOWY

    # API Routes
    path("emails/", views.compose, name="compose"),  # Tworzenie nowego emaila
    path("emails/<int:email_id>/", views.email_view, name="email"),  # Widok pojedynczego emaila
    path("mailbox/<str:mailbox>/", views.mailbox, name="mailbox"),  # inbox, sent, archive
]
