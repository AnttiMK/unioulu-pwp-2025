from django.core.exceptions import ObjectDoesNotExist
from django.test import TransactionTestCase
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import (
    JsonResponse,
    HttpResponseNotFound,
    HttpResponseBadRequest,
    HttpResponseServerError,
    HttpResponse
)
from ..models import Order, User, OrderItem, MenuItem


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

@csrf_exempt
def create_order(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Only POST is allowed.")

    try:
        data = json.loads(request.body)
        user_name = data.get("user")
        order_items = data.get("order_items")
        status = data.get("status", "pending")

        if not user_name or not order_items:
            return HttpResponseBadRequest("Missing required fields: user and order_items.")

        try:
            user = User.objects.get(name=user_name)
        except User.DoesNotExist:
            return HttpResponseNotFound("User not found.")

        new_order = Order.objects.create(user=user, status=status,)

        for item in order_items:
            item_id = item.get("item_id")
            amount = item.get("amount")

            try:
                menu_item = MenuItem.objects.get(id=item_id)
            except MenuItem.DoesNotExist:
                return HttpResponseBadRequest(f"Menu item with id {item_id} not found.")

            OrderItem.objects.create(order=new_order, item=menu_item, amount=amount,)

        return JsonResponse(new_order.serialize(), status=201)

    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON format.")
    except Exception as e:
        return HttpResponseServerError(f"Error creating order: {str(e)}")
@csrf_exempt    
def update_order(request, id):
    if request.method not in ["PUT"]:
        return HttpResponseBadRequest("Only PUT is allowed.")
    try:
        try:
            order = Order.objects.get(id=id)
        except Order.DoesNotExist:
            return HttpResponseNotFound("Order not found.")

        data = json.loads(request.body)
        status = data.get("status")
        order_items = data.get("order_items")

        if status:
            order.status = status

        if order_items:
            for item in order_items:
                item_id = item.get("item_id")
                amount = item.get("amount")
                try:
                    menu_item = MenuItem.objects.get(id=item_id)
                except MenuItem.DoesNotExist:
                    return HttpResponseBadRequest(f"Menu item with id {item_id} not found.")
                try:
                    order_item = OrderItem.objects.get(order=order, item=menu_item)
                    order_item.amount = amount
                    order_item.save()
                except OrderItem.DoesNotExist:
                    OrderItem.objects.create(order=order, item=menu_item, amount=amount,)
        order.save()
        return JsonResponse(order.serialize(), status=200)

    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON format.")
    except Exception as e:
        return HttpResponseServerError(f"Error updating order: {str(e)}")
@csrf_exempt   
def delete_order(request, id):
    if request.method != "DELETE":
        return HttpResponseBadRequest("Only DELETE is allowed.")

    try:
        try:
            order = Order.objects.get(id=id)
        except Order.DoesNotExist:
            return HttpResponseNotFound("Order not found.")
        order.order_items.all().delete()
        order.delete()
        return JsonResponse({"message": "Order deleted successfully."}, status=204)

    except Exception as e:
        return HttpResponseServerError(f"Error deleting order: {str(e)}")