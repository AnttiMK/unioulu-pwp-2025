from django.core.exceptions import ObjectDoesNotExist
from ..models import User
from django.http import (
    JsonResponse,
    HttpResponseNotFound,
)


def get_all(_):
    """
    Returns all users in the database.

    Args:
        _ (HttpRequest): Django HTTP request object (unused)

    Returns:
        JsonResponse: JSON containing all users with a short representation and total count
    """
    users = {"user_count": 0, "users": []}
    for user in User.objects.all():
        users["users"].append(user.serialize(short=True))
        users["user_count"] += 1
    return JsonResponse(users)


def get_by_identifier(_, user_identifier):
    """
    Returns a specific user by their ID or name.

    Args:
        _ (HttpRequest): Django HTTP request object (unused)
        user_identifier (str): User ID (numeric) or name to search for

    Returns:
        JsonResponse: JSON containing the requested user's detailed information
    """
    try:
        if user_identifier.isdigit():
            user = User.objects.get(id=int(user_identifier))
        else:
            user = User.objects.get(name=user_identifier)
    except ObjectDoesNotExist:
        return HttpResponseNotFound("User does not exist!")

    return JsonResponse(user.serialize())


def create_user(request, id):
    pass


def delete_user(request, id):
    pass
