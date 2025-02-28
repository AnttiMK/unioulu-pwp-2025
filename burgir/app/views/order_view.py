from django.core.exceptions import ObjectDoesNotExist
from django.http import (
    JsonResponse,
    HttpResponseNotFound,
    HttpResponseBadRequest,
)
from ..models import Order, User


def get_all(_):
    """
    Returns all orders in the database grouped by status.

    Args:
        _ (HttpRequest): Django HTTP request object (unused)

    Returns:
        JsonResponse: JSON containing all orders organized by their status
    """
    all_orders = Order.objects.all()
    order_by_status = {}
    orders = {"order_count": 0}
    for order in all_orders:
        if order.status not in order_by_status:
            order_by_status[order.status] = []  # Create a new list for this type
        order_by_status[order.status].append(order.serialize(short=True))
        orders["order_count"] += 1

    orders["orders"] = order_by_status

    return JsonResponse(orders)


def get_by_status(_, status):
    """
    Returns the order with a specific status.

    Args:
        _ (HttpRequest): Django HTTP request object (unused)
        status (str): Expects order status, valid status are
        "ready", "preparing", "pending", "registered".

    Returns:
        JsonResponse: JSON containing all the orders with the specified status
    """
    valid_status = ["ready", "preparing", "pending", "registered"]
    if status.lower() not in valid_status:
        return HttpResponseBadRequest(f"Valid status are: {valid_status}")

    orders = {"order_count": 0, "orders": []}
    for order in Order.objects.filter(status=status.lower()):
        orders["order_count"] += 1
        orders["orders"].append(order.serialize())
    return JsonResponse(orders)


def get_by_id(_, order_id: int):
    """
    Returns the order with a specific id.

    Args:
        _ (HttpRequest): Django HTTP request object (unused)
        order_id (int): Order id to find.

    Returns:
        JsonResponse: JSON representation of the order with specified id.
    """
    try:
        order = Order.objects.get(id=int(order_id))
    except ObjectDoesNotExist:
        return HttpResponseNotFound(f"No order found for order number {order_id}!")

    return JsonResponse(order.serialize())


def get_by_user(_, user_name: str):
    """
    Returns the orders made by the specified user.

    Args:
        _ (HttpRequest): Django HTTP request object (unused)
        user (str): The name of the user, who's orders to find.

    Returns:
        JsonResponse: JSON containing all the orders made by this user.
    """
    try:
        user = User.objects.get(name=user_name)
    except ObjectDoesNotExist:
        return HttpResponseNotFound(f"User {user_name} not found!")

    orders = {"user": user.name, "orders": []}
    for order in Order.objects.filter(user=user).all():
        orders["orders"].append(order.serialize())

    return JsonResponse(orders)


def create_order(request, id):
    pass


def update_order(request, id):
    pass


def delete_order(request, id):
    pass
