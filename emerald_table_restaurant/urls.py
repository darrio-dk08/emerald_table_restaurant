"""
URL configuration for emerald_table_restaurant project.
"""

from django.contrib import admin
from django.urls import path
from restaurant import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('booking/', views.booking, name='booking'),
    path('booking/success/', views.booking_success, name='booking_success'),
    path('bookings/', views.booking_list, name='booking_list'),
    path(
        'booking/edit/<int:booking_id>/',
        views.edit_booking,
        name='edit_booking',
    ),
    path(
        'booking/delete/<int:booking_id>/',
        views.delete_booking,
        name='delete_booking',
    ),
]
