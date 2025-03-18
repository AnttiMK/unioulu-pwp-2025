"""Views for managing users."""
import json

from django.core.exceptions import ObjectDoesNotExist
from django.http import (
    HttpResponseNotAllowed,
    JsonResponse,
    HttpResponseNotFound,
    HttpResponseBadRequest,
    HttpResponseServerError,
    HttpResponse,
)
from django.views.decorators.csrf import csrf_exempt

from ..models import User


def get_all(request):
    """
    Returns all users in the database.

    Args:
        request (HttpRequest): Django HTTP request object

    Returns:
        JsonResponse: JSON containing all users with a short representation and total count
    """
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"], "Only GET is allowed!")

    users = {"user_count": 0, "users": []}
    for user in User.objects.all():
        users["users"].append(user.serialize(short=True))
        users["user_count"] += 1
    return JsonResponse(users)


def get_by_identifier(request, user_identifier):
    """
    Returns a specific user by their ID or name.

    Args:
        request (HttpRequest): Django HTTP request object
        user_identifier (str): User ID (numeric) or name to search for

    Returns:
        JsonResponse: JSON containing the requested user's detailed information
    """
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"], "Only GET is allowed!")

    try:
        if user_identifier.isdigit():
            user = User.objects.get(id=int(user_identifier))
        else:
            user = User.objects.get(name=user_identifier)
    except ObjectDoesNotExist:
        return HttpResponseNotFound("User does not exist!")

    return JsonResponse(user.serialize())


@csrf_exempt
def create_user(request):
    """
    Creates a new user.

    Args:
        request (HttpRequest): Django HTTP request object

    Returns:
        JsonResponse: JSON containing the newly created user
    """
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"], "Only POST is allowed!")

    try:
        data = json.loads(request.body)
        name = data.get("name")

        if not name:
            return HttpResponseBadRequest("Missing required field: 'name'.")

        if User.objects.filter(name=name).exists():
            return HttpResponseBadRequest("User with this name already exists.")

        newuser = User.objects.create(name=name)
        return JsonResponse(newuser.serialize(), status=201)

    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON format.")
    except Exception as e:
        return HttpResponseServerError(f"Error creating user: {str(e)}")


@csrf_exempt
def delete_user(request, user_id):
    """Deletes a user by their ID."""
    if request.method != "DELETE":
        return HttpResponseNotAllowed(["PUT"], "Only PUT is allowed!")

    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return HttpResponse(f"User {user_id} deleted successfully.", status=200)

    except User.DoesNotExist:
        return HttpResponseNotFound(f"User with ID {user_id} not found.")
    except Exception as e:
        return HttpResponseServerError(f"Error deleting user: {str(e)}")
