from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Listing, Bid, Comment, User, Category  # Dodajemy import Category

# Formularz do tworzenia aukcji
class CreateListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "starting_bid", "image_url", "category"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "starting_bid": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "image_url": forms.URLInput(attrs={"class": "form-control"}),
        }

    # Zmiana pola 'category' na ModelChoiceField
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="Choose a category"  # Informacja dla użytkownika
    )

    def clean_starting_bid(self):
        starting_bid = self.cleaned_data.get("starting_bid")
        if starting_bid <= 0:
            raise forms.ValidationError("Starting bid must be a positive value.")
        return starting_bid


# Formularz do składania ofert
class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["amount"]
        widgets = {
            "amount": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
        }

    def __init__(self, *args, **kwargs):
        self.listing = kwargs.pop("listing", None)
        super().__init__(*args, **kwargs)

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")
        if amount <= 0:
            raise forms.ValidationError("Bid amount must be greater than zero.")
        if self.listing and amount <= self.listing.current_price():
            raise forms.ValidationError(f"Bid must be higher than current price (${self.listing.current_price()}).")
        return amount


# Formularz do komentarzy
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }


# Formularz rejestracji użytkownika
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"class": "form-control"}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={"class": "form-control"}),
        }

    # Dodatkowe walidacje, jeśli chcesz
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email
