

# Create your views here.
from django.shortcuts import render, redirect
from .models import MenuItem
from .forms import BookingForm

def home(request):
    return render(request, 'restaurant/index.html')

def menu(request):
    items = MenuItem.objects.all()
    return render(request, 'restaurant/menu.html', {'menu_items': items})

def booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BookingForm()
    return render(request, 'restaurant/booking.html', {'form': form})
