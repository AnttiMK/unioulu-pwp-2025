from django.http import JsonResponse
from ..models import MenuItem


def get_menu(_):
    """
    Returns the complete menu with items grouped by type.

    Args:
        _ (HttpRequest): Django HTTP request object (unused)

    Returns:
        JsonResponse: JSON containing all menu items organized by their type
    """
    # get whole menu
    menu_items = MenuItem.objects.all()
    # Group items by type
    menu_by_type = {}
    for item in menu_items:
        if item.type not in menu_by_type:
            menu_by_type[item.type] = []  # Create a new list for this type
        menu_by_type[item.type].append(item.serialize())

    return JsonResponse(menu_by_type)


def get_items_by_type(_, menu_item_type: str):
    """
    Returns menu items filtered by their type.

    Args:
        _ (HttpRequest): Django HTTP request object (unused)
        menu_item_type (str): The type of menu items to filter by (e.g., "drink", "main course")

    Returns:
        JsonResponse: JSON containing all menu items of the specified type
    """
    items = {"type": menu_item_type, "items": []}
    for item in MenuItem.objects.filter(type=menu_item_type).all():
        items["items"].append(item.serialize())

    return JsonResponse(items)


def create_menu_item(request, id):
    pass


def update_menu_item(request, id):
    pass


def delete_menu_item(request, id):
    pass
