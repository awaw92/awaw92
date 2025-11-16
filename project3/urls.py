"""project3 URL Configuration

The `urlpatterns` list routes URLs to views.
For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Wszystkie URL-e aplikacji mail (w tym logowanie i rejestracja)
    path('', include('mail.urls')),  # Kiedy wejdziemy na /login, kierujemy do mail.urls
]
