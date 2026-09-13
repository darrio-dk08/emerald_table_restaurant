from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_safe

from .forms import BookingForm
from .models import Booking, MenuItem


@require_safe
def home(request):
    return render(request, "restaurant/index.html")


@require_safe
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

            if category == "Starter":
                category = "Starters"

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


@require_http_methods(["GET", "POST"])
def signup(request):
    if request.user.is_authenticated:
        return redirect("booking_list")

    form = UserCreationForm(
        request.POST if request.method == "POST" else None
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Account created. Please log in.")
        return redirect("login")

    return render(request, "registration/signup.html", {"form": form})


@login_required
@require_http_methods(["GET", "POST"])
def booking(request):
    instance = Booking(owner=request.user)

    form = BookingForm(
        request.POST if request.method == "POST" else None,
        instance=instance,
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Booking created.")
        return redirect("booking_success")

    return render(request, "restaurant/booking.html", {"form": form})


@login_required
@require_safe
def booking_success(request):
    return render(request, "restaurant/booking_success.html")


@login_required
@require_safe
def booking_list(request):
    bookings = Booking.objects.filter(owner=request.user).order_by(
        "date",
        "time",
        "pk",
    )

    return render(
        request,
        "restaurant/booking_list.html",
        {"bookings": bookings},
    )


@login_required
@require_http_methods(["GET", "POST"])
def edit_booking(request, booking_id):
    instance = get_object_or_404(
        Booking,
        pk=booking_id,
        owner=request.user,
    )

    form = BookingForm(
        request.POST if request.method == "POST" else None,
        instance=instance,
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Booking updated.")
        return redirect("booking_list")

    return render(request, "restaurant/edit_booking.html", {"form": form})


@login_required
@require_http_methods(["GET", "POST"])
def delete_booking(request, booking_id):
    instance = get_object_or_404(
        Booking,
        pk=booking_id,
        owner=request.user,
    )

    if request.method == "POST":
        instance.delete()
        messages.success(request, "Booking deleted.")
        return redirect("booking_list")

    return render(
        request,
        "restaurant/delete_booking.html",
        {"booking": instance},
    )