import os
from pathlib import Path

# Ścieżka do katalogu głównego projektu
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-your-secret-key-here'

# W trybie deweloperskim ustawiamy DEBUG = True
DEBUG = True

# Wartości produkcyjne powinny zawierać dozwolone hosty
ALLOWED_HOSTS = []  # W produkcji ustaw to na domeny, np. ['yourdomain.com']

# Aplikacje Django i Twoja aplikacja
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'auctions',  # Twoja aplikacja 'auctions'
    'commerce',  # Twoja aplikacja 'commerce' (dodana aplikacja 'commerce')
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'commerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # globalny katalog szablonów
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'commerce.wsgi.application'

# Baza danych SQLite (prosta do testów)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Hasła
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Język i strefa czasowa
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'  # Możesz zmienić na swoją strefę czasową, np. 'Europe/Warsaw'
USE_I18N = True
USE_TZ = True

# Statyczne pliki
STATIC_URL = '/static/'

# Nowe ustawienia statycznych plików
STATICFILES_DIRS = [
    BASE_DIR / 'static',  # Ścieżka do katalogu, gdzie przechowujesz pliki statyczne w trakcie rozwoju
]

STATIC_ROOT = BASE_DIR / 'staticfiles'  # Folder, do którego Django zbierze pliki statyczne po uruchomieniu collectstatic

# Używasz własnego modelu użytkownika
AUTH_USER_MODEL = 'auctions.User'

# Ustawienia logowania
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

# Domyślne pole AutoField
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

