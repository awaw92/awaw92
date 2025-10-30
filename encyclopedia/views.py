from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import random
import markdown2  # import do konwersji markdown na HTML

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "Strona nie istnieje."
        })
    else:
        html_content = markdown2.markdown(content)  # konwersja Markdown do HTML
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })


def search(request):
    query = request.GET.get("q", "")
    entries = util.list_entries()
    results = [entry for entry in entries if query.lower() in entry.lower()]

    # Jeśli jest dokładne dopasowanie (niezależne od wielkości liter), przekieruj do wpisu
    for entry in entries:
        if entry.lower() == query.lower():
            return redirect("entry", title=entry)

    return render(request, "encyclopedia/search.html", {
        "results": results,
        "query": query
    })


def create(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "")

        entries = util.list_entries()
        # Sprawdzanie niezależne od wielkości liter
        if any(entry.lower() == title.lower() for entry in entries):
            return render(request, "encyclopedia/create.html", {
                "error": "Strona o takiej nazwie już istnieje.",
                "title": title,
                "content": content
            })
        else:
            util.save_entry(title, content)
            return redirect("entry", title=title)

    return render(request, "encyclopedia/create.html")


def random_entry(request):
    entries = util.list_entries()
    if not entries:
        return render(request, "encyclopedia/error.html", {
            "message": "Brak dostępnych wpisów."
        })
    random_title = random.choice(entries)
    return redirect("entry", title=random_title)


def edit_entry(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "Strona nie istnieje i nie można jej edytować."
        })

    if request.method == "POST":
        updated_content = request.POST.get("content", "")
        util.save_entry(title, updated_content)
        return redirect("entry", title=title)

    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })
