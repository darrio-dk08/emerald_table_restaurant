from collections import OrderedDict

from django.shortcuts import render, redirect

from .forms import BookingForm
from .models import MenuItem


def home(request):
    return render(request, "restaurant/index.html")


def menu(request):
    # The current model doesn't have a "category" field, so we infer it from the
    # name convention: "Starter - Burrata & Citrus", "Mains - Steak Frites", etc.
    items = MenuItem.objects.all().order_by("name")

    grouped = OrderedDict()
    for item in items:
        raw = (item.name or "").strip()
        if " - " in raw:
            category, title = raw.split(" - ", 1)
            category = category.strip()
            title = title.strip()
        else:
            category = "Menu"
            title = raw

        grouped.setdefault(category, []).append(
            {
                "title": title,
                "description": item.description,
                "price": item.price,
            }
        )

    return render(request, "restaurant/menu.html", {"grouped_menu": grouped.items()})


def booking(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = BookingForm()
    return render(request, "restaurant/booking.html", {"form": form})