from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Panel admina
    path('', include('auctions.urls')),  # Teraz strona główna = index
]
