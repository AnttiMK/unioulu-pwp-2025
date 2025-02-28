from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from ..models import Reservation, User
from django.http import (
    JsonResponse,
    HttpResponseNotFound,
    HttpResponseBadRequest,
)


def get_all(_):
    """
    Returns all reservations in the database.

    Args:
        _ (HttpRequest): Django HTTP request object (unused)

    Returns:
        JsonResponse: JSON containing all reservations with their count
    """
    reservations = {"reservation_count": 0, "reservations": []}

    for reservation in Reservation.objects.all():
        reservations["reservation_count"] += 1
        reservations["reservations"].append(reservation.serialize())

    return JsonResponse(reservations)


def get_by_time_status(_, time_status: str):
    """
    Returns reservations filtered by their time status (upcoming, current, or past).

    Args:
        _ (HttpRequest): Django HTTP request object (unused)
        time_status (str): The time status - "upcoming", "current" or "past"

    Returns:
        JsonResponse: JSON containing all reservations with the specified time status
    """

    valid_time_status = ["upcoming", "current", "past"]
    if time_status not in valid_time_status:
        return HttpResponseBadRequest(f"Time must be one of: {valid_time_status}")
    reservations = {"reservation_count": 0, "reservations": []}

    current_time = datetime.now()

    # not done
    if time_status == "upcoming":
        query = Reservation.objects.filter(date_and_time__gt=current_time).all()
    elif time_status == "current":
        query = Reservation.objects.exclude(date_and_time__gt=current_time).exclude(
            date_and_time__lt=current_time
        )
    else:
        query = Reservation.objects.filter(date_and_time__lt=current_time)

    for reservation in query:
        reservations["reservation_count"] += 1
        reservations["reservations"].append(reservation.serialize())

    return JsonResponse(reservations)


def get_by_id(_, reservation_id: int):
    """
    Returns a specific reservation by its ID.

    Args:
        _ (HttpRequest): Django HTTP request object (unused)
        reservation_id (int): The unique identifier of the reservation

    Returns:
        JsonResponse: JSON containing the requested reservation details
    """
    try:
        reservation = Reservation.objects.get(id=int(reservation_id))
    except ObjectDoesNotExist:
        return HttpResponseNotFound(
            f"Reservation with number {reservation_id} not found!"
        )

    return JsonResponse(reservation.serialize())


def get_by_user(_, user_name: str):
    """
    Returns all reservations for a specific user.

    Args:
        _ (HttpRequest): Django HTTP request object (unused)
        user_name (str): Username to filter reservations by

    Returns:
        JsonResponse: JSON containing all reservations for the specified user
    """
    try:
        user = User.objects.get(name=user_name)
    except ObjectDoesNotExist:
        return HttpResponseNotFound(f"User {user_name} does not exist")

    reservations = {"user": user.name, "reservations": []}
    for reservation in Reservation.objects.filter(user=user).all():
        reservations["reservations"].append(reservation.serialize())

    return JsonResponse(reservations)


def create_reservation(request, id):
    pass


def update_reservation(request, id):
    pass


def delete_reservation(request, id):
    pass
