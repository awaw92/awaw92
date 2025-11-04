from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Listing, Bid, Comment, Watchlist, Category
from .forms import CreateListingForm, BidForm, CommentForm, UserRegisterForm

def is_listing_owner(user, listing):
    return user == listing.owner

def index(request):
    # Pobieramy WSZYSTKIE aukcje, nie tylko aktywne
    listings = Listing.objects.all().order_by('-created_at')
    watchlist_count = Watchlist.objects.filter(user=request.user).count() if request.user.is_authenticated else 0
    categories = Category.objects.all()
    
    return render(request, "auctions/index.html", {
        "listings": listings,
        "watchlist_count": watchlist_count,
        "categories": categories,
    })

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Konto zostało utworzone pomyślnie! Zostałeś zalogowany.")
            return redirect("auctions:index")
        else:
            messages.error(request, "Wystąpił błąd podczas rejestracji. Sprawdź dane.")
    else:
        form = UserRegisterForm()
    return render(request, "auctions/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Witaj, {username}!")
            return redirect(request.GET.get('next', 'auctions:index'))
        else:
            messages.error(request, "Nieprawidłowa nazwa użytkownika lub hasło.")
            return render(request, "auctions/login.html", {"username": username})
    return render(request, "auctions/login.html")

def logout_view(request):
    logout(request)
    messages.info(request, "Zostałeś wylogowany.")
    return redirect("auctions:index")

@login_required
def create_listing(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            messages.success(request, "Ogłoszenie zostało utworzone!")
            return redirect("auctions:index")
        else:
            messages.error(request, "Wystąpił błąd w formularzu. Sprawdź dane.")
    else:
        form = CreateListingForm()
    return render(request, "auctions/create_listing.html", {"form": form})

@login_required
def listing_detail(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    comments = listing.comments.all()
    bid_form = BidForm()
    comment_form = CommentForm()
    in_watchlist = Watchlist.objects.filter(user=request.user, listing=listing).exists()

    bids = listing.bids.order_by('id')
    current_price = listing.starting_bid
    bid_attempt_number = bids.count()
    highest_bid = bids.last() if bids.exists() else None
    if highest_bid:
        current_price = highest_bid.amount

    winner = highest_bid.bidder if highest_bid and not listing.active else None
    watchlist_count = Watchlist.objects.filter(user=request.user).count() if request.user.is_authenticated else 0

    if request.method == "POST":
        if "place_bid" in request.POST:
            bid_form = BidForm(request.POST)
            if bid_form.is_valid():
                bid = bid_form.save(commit=False)
                bid.listing = listing
                bid.bidder = request.user
                if not listing.active:
                    messages.error(request, "Aukcja została zakończona. Nie można licytować ani komentować.")
                elif bid.amount > current_price:
                    bid.save()
                    messages.success(request, "Oferta została złożona pomyślnie!")
                    current_price = bid.amount
                    bid_attempt_number += 1
                    highest_bid = bid
                else:
                    messages.error(request, "Twoja oferta musi być wyższa niż aktualna cena.")
            else:
                messages.error(request, "Błąd w formularzu oferty.")

        elif "add_comment" in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.listing = listing
                comment.commenter = request.user
                comment.save()
                messages.success(request, "Komentarz został dodany!")
                comments = listing.comments.all()
            else:
                messages.error(request, "Błąd w formularzu komentarza.")

        elif "close_auction" in request.POST:
            if is_listing_owner(request.user, listing):
                listing.active = False
                listing.save()
                messages.success(request, "Aukcja zakończona!")
                winner = highest_bid.bidder if highest_bid else None
            else:
                messages.error(request, "Nie masz uprawnień do zamknięcia tej aukcji.")

    context = {
        "listing": listing,
        "bid_form": bid_form,
        "comment_form": comment_form,
        "comments": comments,
        "in_watchlist": in_watchlist,
        "winner": winner,
        "current_price": current_price,
        "bid_attempt_number": bid_attempt_number,
        "watchlist_count": watchlist_count,
    }
    return render(request, "auctions/listing_detail.html", context)

# ---------------- Funkcje watchlist ----------------

@login_required
def add_to_watchlist(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    Watchlist.objects.get_or_create(user=request.user, listing=listing)
    messages.success(request, "Dodano do watchlisty!")
    return redirect('auctions:listing_detail', listing_id=listing.id)

@login_required
def remove_from_watchlist(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    Watchlist.objects.filter(user=request.user, listing=listing).delete()
    messages.success(request, "Usunięto z watchlisty!")
    return redirect('auctions:listing_detail', listing_id=listing.id)

@login_required
def view_watchlist(request):
    items = request.user.watchlist_items.all()
    watchlist_count = items.count()
    return render(request, 'auctions/watchlist.html', {
        'items': items,
        'watchlist_count': watchlist_count,
    })

# ---------------- Edycja i usuwanie aukcji ----------------

@login_required
def edit_listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    if not is_listing_owner(request.user, listing):
        messages.error(request, "Nie masz uprawnień do edycji tego ogłoszenia.")
        return redirect('auctions:listing_detail', listing_id=listing.id)

    if request.method == "POST":
        form = CreateListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            messages.success(request, "Ogłoszenie zaktualizowane!")
            return redirect('auctions:listing_detail', listing_id=listing.id)
        else:
            messages.error(request, "Błąd w formularzu. Sprawdź dane.")
    else:
        form = CreateListingForm(instance=listing)

    return render(request, "auctions/edit_listing.html", {
        "form": form,
        "listing": listing,
        "hide_navbar": True
    })

@login_required
def delete_listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    if not is_listing_owner(request.user, listing):
        messages.error(request, "Nie masz uprawnień do usunięcia tego ogłoszenia.")
        return redirect('auctions:listing_detail', listing_id=listing.id)

    if request.method == "POST":
        listing.delete()
        messages.success(request, "Ogłoszenie usunięte!")
        return redirect('auctions:index')

    return render(request, "auctions/confirm_delete.html", {"listing": listing})

@login_required
def user_profile(request):
    user = request.user
    user_listings = Listing.objects.filter(owner=user)
    return render(request, "auctions/user_profile.html", {"user": user, "listings": user_listings})

# ---------------- Widok kategorii ----------------

def category_list(request):
    categories = Category.objects.all()
    category_data = [{
        'category': category,
        'listing_count': Listing.objects.filter(category=category).count()  # uwaga: wszystkie aukcje, nie tylko aktywne
    } for category in categories]
    return render(request, "auctions/category_list.html", {"categories": category_data})

def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    listings = Listing.objects.filter(category=category).order_by('-created_at')  # wszystkie, nie tylko aktywne
    return render(request, "auctions/category_detail.html", {
        "category": category,
        "listings": listings,
        "listing_count": listings.count(),
        "is_category_page": True,
    })
