from django.shortcuts import render
from .models import Table, Reservation, MenuItem, Order

# Create your views here.
def home(request):
    return render(request, "home.html")

def tables(request):
    tables = Table.objects.all()
    return render(request, "tablelist.html", {"tables": tables})

def menu(request):
    menu_items = MenuItem.objects.all()
    
    # Group items by type
    menu_by_type = {}
    for item in menu_items:
        if item.type not in menu_by_type:
            menu_by_type[item.type] = []  # Create a new list for this type
        menu_by_type[item.type].append(item)

    return render(request, "menu.html", {"menu_by_type": menu_by_type})

def reservations(request):
    reservations = Reservation.objects.all()
    return render(request, "user_reservations.html", {"reservations": reservations})

def orders(request):
    orders = Order.objects.all()
    return render(request, "orders.html", {"orders": orders})
