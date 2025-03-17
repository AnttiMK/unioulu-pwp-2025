import json

from django.http import (
    JsonResponse,
    HttpResponseBadRequest,
    HttpResponseNotAllowed,
    HttpResponseServerError
)

from ..models import MenuItem


def get_menu(request):
    """
    Returns the complete menu with items grouped by type.

    Args:
        request (HttpRequest): Django HTTP request object

    Returns:
        JsonResponse: JSON containing all menu items organized by their type
    """
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"], "Only GET is allowed!")

    # get whole menu
    menu_items = MenuItem.objects.all()
    # Group items by type
    menu_by_type = {}
    for item in menu_items:
        if item.type not in menu_by_type:
            menu_by_type[item.type] = []  # Create a new list for this type
        menu_by_type[item.type].append(item.serialize())

    return JsonResponse(menu_by_type)


def get_items_by_type(request, menu_item_type: str):
    """
    Returns menu items filtered by their type.

    Args:
        request (HttpRequest): Django HTTP request object
        menu_item_type (str): The type of menu items to filter by (e.g., "drink", "main course")

    Returns:
        JsonResponse: JSON containing all menu items of the specified type
    """
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"], "Only GET is allowed!")

    items = {"type": menu_item_type, "items": []}
    for item in MenuItem.objects.filter(type=menu_item_type).all():
        items["items"].append(item.serialize())

    return JsonResponse(items)


def create_menu_item(request):
    """

    """
    if request.method != "POST":
        return HttpResponseBadRequest("Only POST is allowed.")

    try:
        data = json.loads(request.body)
        name = data.get("name")
        description = data.get("description")
        item_type = data.get("type")
        price = data.get("price")

        if not (name and description and item_type and price):
            return HttpResponseBadRequest("Missing required fields")

        if MenuItem.objects.filter(name=name).exists():
            return HttpResponseBadRequest("Menu item with this name already exists.")

        new_item = MenuItem.objects.create(
            name=name, description=description, type=item_type, price=price
        )
        return JsonResponse(new_item.serialize(), status=201)

    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON format.")
    except Exception as e:
        return HttpResponseServerError(f"Error creating user: {str(e)}")


# def update_menu_item(request, id):
#     pass


# def delete_menu_item(request, id):
#    pass
