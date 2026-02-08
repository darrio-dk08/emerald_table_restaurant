from collections import OrderedDict
from django.shortcuts import render, redirect

from .forms import BookingForm
from .models import MenuItem


def home(request):
    return render(request, "restaurant/index.html")


def menu(request):
    items = MenuItem.objects.all().order_by("name")

    category_descriptions = {
        "Starters": "Light, bright and shareable.",
        "Starter": "Light, bright and shareable.",
        "Mains": "Comfort classics with a fresh emerald twist.",
        "Pasta": "Hand-finished sauces, made to order.",
        "Desserts": "Sweet endings, not too heavy.",
        "Drinks": "Seasonal cocktails and crisp classics.",
        "Menu": "Seasonal favourites, prepared fresh daily.",
    }

    # Your desired order
    category_order = ["Starters", "Mains", "Pasta", "Desserts", "Drinks"]

    grouped = {}
    unknown_categories = {}

    for item in items:
        raw = (item.name or "").strip()

        if " - " in raw:
            category, title = raw.split(" - ", 1)
            category = category.strip()
            title = title.strip()
        else:
            category = "Menu"
            title = raw

        entry = {"title": title,
                 "description": item.description, "price": item.price}

        if category in category_order:
            grouped.setdefault(category, []).append(entry)
        else:
            unknown_categories.setdefault(category, []).append(entry)

    # Build ordered sections
    sections = []

    # First: ordered categories
    for cat in category_order:
        if cat in grouped:
            sections.append(
                {
                    "title": cat,
                    "description": category_descriptions.get(cat, ""),
                    "items": grouped[cat],
                }
            )

    # Then: any unknown categories at the bottom
    for cat, items_list in unknown_categories.items():
        sections.append(
            {
                "title": cat,
                "description": category_descriptions.get(cat, ""),
                "items": items_list,
            }
        )

    return render(request, "restaurant/menu.html", {"menu_sections": sections})


def booking(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("booking_success")
    else:
        form = BookingForm()

    return render(request, "restaurant/booking.html", {"form": form})


def booking_success(request):
    return render(request, "restaurant/booking_success.html")
