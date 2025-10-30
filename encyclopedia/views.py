from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import random
import markdown2  # import do konwersji markdown na HTML

from . import util


def index(request):
    """
    Wyświetla stronę główną z listą dostępnych wpisów.
    """
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    """
    Wyświetla pojedynczy wpis. Jeśli wpis nie istnieje, wyświetla stronę błędu.
    """
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "Strona o tytule '{}' nie istnieje.".format(title)
        })
    else:
        html_content = markdown2.markdown(content)  # Konwersja Markdown na HTML
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })


def search(request):
    """
    Wyszukuje wpisy pasujące do zapytania.
    Jeśli jest dokładne dopasowanie do tytułu, przekierowuje bezpośrednio na stronę tego wpisu.
    """
    query = request.GET.get("q", "").strip()
    entries = util.list_entries()

    # Jeśli zapytanie jest puste, wyświetlamy stronę wyszukiwania z pustym wynikiem
    if not query:
        return render(request, "encyclopedia/search.html", {
            "results": [],
            "query": query
        })

    # Filtrujemy wyniki wyszukiwania (niezależnie od wielkości liter)
    results = [entry for entry in entries if query.lower() in entry.lower()]

    # Jeśli jest dokładne dopasowanie, przekierowujemy do tego wpisu
    for entry in entries:
        if entry.lower() == query.lower():
            return redirect("entry", title=entry)

    return render(request, "encyclopedia/search.html", {
        "results": results,
        "query": query
    })


def create(request):
    """
    Tworzy nowy wpis na podstawie formularza. Sprawdza, czy wpis o tej nazwie już istnieje.
    """
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()

        # Sprawdzanie, czy strona o takiej nazwie już istnieje (niezależnie od wielkości liter)
        entries = util.list_entries()
        if any(entry.lower() == title.lower() for entry in entries):
            return render(request, "encyclopedia/create.html", {
                "error": "Strona o takiej nazwie już istnieje.",
                "title": title,
                "content": content
            })
        else:
            # Zapisujemy nowy wpis
            util.save_entry(title, content)
            return redirect("entry", title=title)

    return render(request, "encyclopedia/create.html")


def random_entry(request):
    """
    Wybiera losowy wpis z dostępnych stron.
    """
    entries = util.list_entries()
    if not entries:
        return render(request, "encyclopedia/error.html", {
            "message": "Brak dostępnych wpisów."
        })

    # Wybieramy losowy tytuł i przekierowujemy na stronę tego wpisu
    random_title = random.choice(entries)
    return redirect("entry", title=random_title)


def edit_entry(request, title):
    """
    Edytuje istniejący wpis. Jeśli wpis nie istnieje, wyświetla stronę błędu.
    """
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "Strona '{}' nie istnieje i nie można jej edytować.".format(title)
        })

    if request.method == "POST":
        updated_content = request.POST.get("content", "").strip()

        # Zapisujemy zaktualizowaną treść
        util.save_entry(title, updated_content)
        return redirect("entry", title=title)

    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })
