from django.shortcuts import render
from .models import Table, Reservation, MenuItem, Order, User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound


# Create your views here.
def home(request):
    return render(request, "home.html")


def user(request, user):
    try:
        if isinstance(user, str):
            user = User.objects.get(name=user)
        else:
            user = User.objects.get(id=user)
    except ObjectDoesNotExist:
        return HttpResponseNotFound("User does not exist!")
    return JsonResponse(user.serialize())


def users(request):
    users = {"users": [], "user_count": 0}
    for user in User.objects.all():
        users["users"].append(user.serialize(short=True))
        users["user_count"] += 1
    return JsonResponse(users)


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
    return render(request, "reservations.html", {"reservations": reservations})


def reservation(request, user):
    try:
        if isinstance(user, str):
            user = User.objects.get(name=user)
        else:
            user = User.objects.get(id=user)
    except ObjectDoesNotExist:
        return HttpResponseNotFound("User does not exist!")


def reservation_by_id(request, id):
    try:
        reservation = Reservation.objects.get(id=id)
    except ObjectDoesNotExist:
        return render(
            request,
            "not_found.html",
            {"type": "reservation", "query": id},
            status=404,
        )
    return render(
        request, "reservation_by_id.html", {"reservation": reservation}, status=200
    )


def reservations_by_user(request, user_name):
    try:
        user = User.objects.get(name=user_name)
    except ObjectDoesNotExist:
        return render(
            request,
            "not_found.html",
            {"type": "user", "query": user_name},
            status=404,
        )
    reservations = Reservation.objects.filter(user=user).all()
    return render(
        request,
        "reservations_by_user.html",
        {"reservations": reservations, "user_name": user_name},
    )


def orders(request):
    orders = Order.objects.all()
    return render(request, "orders.html", {"orders": orders})


def order_by_id(request, id):
    try:
        order = Order.objects.get(id=id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound(f"No order found for order number {id}!")
    return JsonResponse(order.serialize())


def orders_by_user(request, user_name):
    try:
        user = User.objects.get(name=user_name)
    except ObjectDoesNotExist:
        return HttpResponseNotFound(f"User {user_name} not found!")

    orders = {"user": user_name, "orders": []}
    for order in Order.objects.filter(user=user).all():
        orders["orders"].append(order.serialize())

    return JsonResponse(orders)
