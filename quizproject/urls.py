from django.contrib import admin
from django.urls import path, include  # <- dodaj include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('quiz.urls')),  # <- przekierowuje główny URL do aplikacji quiz
]
