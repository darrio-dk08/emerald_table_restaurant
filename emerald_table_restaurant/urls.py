"""URL configuration for Emerald Table Restaurant."""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from restaurant import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("menu/", views.menu, name="menu"),
    path("accounts/signup/", views.signup, name="signup"),
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(),
        name="login",
    ),
    path(
        "accounts/logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
    path("booking/", views.booking, name="booking"),
    path(
        "booking/success/",
        views.booking_success,
        name="booking_success",
    ),
    path("bookings/", views.booking_list, name="booking_list"),
    path(
        "booking/edit/<int:booking_id>/",
        views.edit_booking,
        name="edit_booking",
    ),
    path(
        "booking/delete/<int:booking_id>/",
        views.delete_booking,
        name="delete_booking",
    ),
]