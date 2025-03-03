from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from ..models import User
import json
from django.http import (
    JsonResponse,
    HttpResponseNotFound,
    HttpResponseBadRequest,
    HttpResponseServerError,
    HttpResponse
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

@csrf_exempt

def create_user(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Only POST is allowed.")

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
def delete_user(request, id):
    if request.method != "DELETE":
        return HttpResponseBadRequest("Only DELETE is allowed.")

    try:
        user = User.objects.get(id=id)
        user.delete()
        return HttpResponse(f"User {id} deleted successfully.", status=200)

    except User.DoesNotExist:
        return HttpResponseNotFound(f"User with ID {id} not found.")
    except Exception as e:
        return HttpResponseServerError(f"Error deleting user: {str(e)}")
