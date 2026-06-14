from django.shortcuts import render, redirect, get_object_or_404

from .forms import BookingForm
from .models import Booking, MenuItem


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

        entry = {
            "title": title,
            "description": item.description,
            "price": item.price,
        }

        if category in category_order:
            grouped.setdefault(category, []).append(entry)
        else:
            unknown_categories.setdefault(category, []).append(entry)

    sections = []

    for cat in category_order:
        if cat in grouped:
            sections.append(
                {
                    "title": cat,
                    "description": category_descriptions.get(cat, ""),
                    "items": grouped[cat],
                }
            )

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


def booking_list(request):
    bookings = Booking.objects.all().order_by("-created_at")

    return render(
        request,
        "restaurant/booking_list.html",
        {"bookings": bookings},
    )


def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == "POST":
        form = BookingForm(request.POST, instance=booking)

        if form.is_valid():
            form.save()
            return redirect("booking_list")
    else:
        form = BookingForm(instance=booking)

    return render(
        request,
        "restaurant/edit_booking.html",
        {"form": form},
    )


def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == "POST":
        booking.delete()
        return redirect("booking_list")

    return render(
        request,
        "restaurant/delete_booking.html",
        {"booking": booking},
    )
