from django.db import models
from django.contrib.auth.models import AbstractUser

# Rozszerzony model użytkownika
class User(AbstractUser):
    pass

# Model kategorii
class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    # Dodajemy domyślne kategorie w metodzie `create_initial_categories`
    @classmethod
    def create_initial_categories(cls):
        categories = ['Cars', 'Trucks', 'Phones']
        for category_name in categories:
            cls.objects.get_or_create(name=category_name)

# Model ogłoszenia/listingu
class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True, null=True)  # Pole na URL do obrazka
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)  # Powiązanie z kategorią
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    created_at = models.DateTimeField(auto_now_add=True)  # Dodanie daty utworzenia aukcji

    def __str__(self):
        return f"{self.title} ({self.starting_bid}) - {'Active' if self.active else 'Closed'}"

    # Metoda zwracająca aktualną cenę aukcji
    def current_price(self):
        highest_bid = self.bids.order_by('-amount').first()  # szukamy najwyższej oferty
        if highest_bid:
            return highest_bid.amount
        return self.starting_bid  # jeśli brak ofert, cena początkowa

    class Meta:
        ordering = ['-created_at']  # Sortowanie po dacie stworzenia (najnowsze aukcje na górze)

# Model oferty (Bid)
class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)  # Dodanie daty utworzenia oferty

    def __str__(self):
        return f"{self.bidder.username} bids {self.amount} on {self.listing.title}"

    class Meta:
        ordering = ["-amount"]  # Najwyższe oferty na górze

# Model komentarza
class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.commenter.username} on {self.listing.title}: {self.content[:20]}"

    class Meta:
        ordering = ["-created_at"]  # Najnowsze komentarze na górze

# Model watchlisty (Lista obserwowanych)
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist_items")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchlisted_by")
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'listing')  # Jeden użytkownik może dodać aukcję tylko raz

    def __str__(self):
        return f"{self.user.username} watches {self.listing.title}"
