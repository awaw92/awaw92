from django.contrib import admin
from .models import Listing, Bid, Comment

# Rejestracja modeli w panelu admina
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)
