"""Views for managing reservations."""
import json
from datetime import datetime, timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import (
    JsonResponse,
    HttpResponseNotFound,
    HttpResponseBadRequest,
    HttpResponseServerError,
    HttpResponseNotAllowed,
)
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from ..models import Reservation, Table, User


def get_all(request):
    """
    Returns all reservations in the database.

    Args:
        request (HttpRequest): Django HTTP request object (unused)

    Returns:
        JsonResponse: JSON containing all reservations with their count
    """
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"], "Only GET is allowed!")

    reservations = {"reservation_count": 0, "reservations": []}

    for reservation in Reservation.objects.all():
        reservations["reservation_count"] += 1
        reservations["reservations"].append(reservation.serialize())

    return JsonResponse(reservations)


def get_by_time_status(request, time_status: str):
    """
    Returns reservations filtered by their time status (upcoming, current, or past).

    Args:
        request (HttpRequest): Django HTTP request object (unused)
        time_status (str): The time status - "upcoming", "current" or "past"

    Returns:
        JsonResponse: JSON containing all reservations with the specified time status
    """
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"], "Only GET is allowed!")

    valid_time_status = ["upcoming", "current", "past"]
    if time_status not in valid_time_status:
        return HttpResponseBadRequest(f"Time must be one of: {valid_time_status}")

    reservations = {"reservation_count": 0, "reservations": []}
    all_reservations = Reservation.objects.all()

    current_time = timezone.now()

    if time_status == "upcoming":
        for reservation in Reservation.objects.filter(
                date_and_time__gt=current_time
        ).all():
            reservations["reservation_count"] += 1
            reservations["reservations"].append(reservation.serialize())

    elif time_status == "current":
        for reservation in all_reservations:
            if reservation.date_and_time > current_time:
                continue
            reservation_end = reservation.date_and_time + reservation.duration
            if reservation_end > current_time:
                reservations["reservation_count"] += 1
                reservations["reservations"].append(reservation.serialize())

    elif time_status == "past":
        for reservation in all_reservations:
            reservation_end = reservation.date_and_time + reservation.duration
            if reservation_end < current_time:
                reservations["reservation_count"] += 1
                reservations["reservations"].append(reservation.serialize())

    return JsonResponse(reservations)


def get_by_id(request, reservation_id: int):
    """
    Returns a specific reservation by its ID.

    Args:
        request (HttpRequest): Django HTTP request object (unused)
        reservation_id (int): The unique identifier of the reservation

    Returns:
        JsonResponse: JSON containing the requested reservation details
    """
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"], "Only GET is allowed!")

    try:
        reservation = Reservation.objects.get(id=int(reservation_id))
    except ObjectDoesNotExist:
        return HttpResponseNotFound(
            f"Reservation with number {reservation_id} not found!"
        )

    return JsonResponse(reservation.serialize())


def get_by_user(request, user_name: str):
    """
    Returns all reservations for a specific user.

    Args:
        request (HttpRequest): Django HTTP request object (unused)
        user_name (str): Username to filter reservations by

    Returns:
        JsonResponse: JSON containing all reservations for the specified user
    """
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"], "Only GET is allowed!")

    try:
        user = User.objects.get(name=user_name)
    except ObjectDoesNotExist:
        return HttpResponseNotFound(f"User {user_name} does not exist")

    reservations = {"user": user.name, "reservations": []}
    for reservation in Reservation.objects.filter(user=user).all():
        reservations["reservations"].append(reservation.serialize())

    return JsonResponse(reservations)


@csrf_exempt
def create_reservation(request):
    """
    Creates a new reservation.

    Args:
        request (HttpRequest): Django HTTP request object

    Returns:
        JsonResponse: JSON containing the newly created reservation
    """
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"], "Only POST is allowed!")

    try:
        data = json.loads(request.body)
        user_name = data.get("reserver")
        table_id = data.get("table")
        number_of_people = data.get("number_of_people")
        date_and_time = data.get("date_and_time")
        duration = data.get("duration")

        if not (
                user_name and table_id and number_of_people and date_and_time and duration
        ):
            return HttpResponseBadRequest("Missing required fields.")
        try:
            user = User.objects.get(name=user_name)
        except User.DoesNotExist:
            return HttpResponseNotFound("User not found.")
        try:
            table = Table.objects.get(id=table_id)
        except Table.DoesNotExist:
            return HttpResponseNotFound("Table not found.")
        naive_datetime = datetime.strptime(date_and_time, "%Y-%m-%d %H:%M:%S")
        aware_datetime = timezone.make_aware(
            naive_datetime, timezone.get_current_timezone()
        )
        hours, minutes, seconds = map(int, duration.split(":"))
        duration_timedelta = timedelta(hours=hours, minutes=minutes, seconds=seconds)

        if aware_datetime < timezone.now():
            return HttpResponseBadRequest("Reservation can't be in the past!")

        if number_of_people < table.min_people:
            return HttpResponseBadRequest(
                f"Too few people for this table. Minimum required: {table.min_people}."
            )
        if number_of_people > table.max_people:
            return HttpResponseBadRequest(
                f"Too many people for this table. Maximum allowed: {table.max_people}."
            )

        end_time = aware_datetime + duration_timedelta
        overlapping = Reservation.objects.filter(
            date_and_time__lt=end_time,
            date_and_time__gte=(aware_datetime - models.F("duration")),
        )

        if overlapping.exists():
            return HttpResponseBadRequest(
                "Reservation overlaps with existing reservations"
            )

        new_reservation = Reservation.objects.create(
            user=user,
            table=table,
            number_of_people=number_of_people,
            date_and_time=aware_datetime,
            duration=duration_timedelta,
        )
        return JsonResponse(new_reservation.serialize(), status=201)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON format.")
    except ValueError:
        return HttpResponseBadRequest("Invalid date/time or duration format.")
    except Exception as e:
        return HttpResponseServerError(f"Error creating reservation: {str(e)}")


@csrf_exempt
def update_reservation(request, reservation_id):
    """
    Updates an existing reservation.

    Args:
        request (HttpRequest): Django HTTP request object
        reservation_id (int): ID of reservation to update

    Returns:
        JsonResponse: JSON containing the updated reservation
    """
    if request.method != "PUT":
        return HttpResponseNotAllowed(["PUT"], "Only PUT is allowed!")

    try:
        data = json.loads(request.body)
        number_of_people = data.get("number_of_people")
        date_and_time = data.get("date_and_time")
        duration = data.get("duration")

        try:
            reservation = Reservation.objects.get(id=reservation_id)
        except Reservation.DoesNotExist:
            return HttpResponseNotFound("Reservation not found.")

        if number_of_people:
            reservation.number_of_people = number_of_people

        if date_and_time:
            naive_datetime = datetime.strptime(date_and_time, "%Y-%m-%d %H:%M:%S")
            aware_datetime = timezone.make_aware(
                naive_datetime, timezone.get_current_timezone()
            )
            reservation.date_and_time = aware_datetime

        if duration:
            hours, minutes, seconds = map(int, duration.split(":"))
            duration_timedelta = timedelta(
                hours=hours, minutes=minutes, seconds=seconds
            )
            reservation.duration = duration_timedelta

        if number_of_people < reservation.table.min_people:
            return HttpResponseBadRequest(
                f"Too few people for this table. Minimum required: {reservation.table.min_people}."
            )
        if number_of_people > reservation.table.max_people:
            return HttpResponseBadRequest(
                f"Too many people for this table. Maximum allowed: {reservation.table.max_people}."
            )

        if aware_datetime < timezone.now():
            return HttpResponseBadRequest("Reservation can't be in the past!")

        end_time = aware_datetime + duration_timedelta
        overlapping = Reservation.objects.filter(
            date_and_time__lt=end_time,
            date_and_time__gte=(aware_datetime - models.F("duration")),
        )

        if overlapping.exists():
            return HttpResponseBadRequest(
                "Reservation overlaps with existing reservations"
            )

        reservation.save()
        return JsonResponse(reservation.serialize(), status=200)

    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON format.")
    except ValueError:
        return HttpResponseBadRequest("Invalid date/time or duration format.")
    except Exception as e:
        return HttpResponseServerError(f"Error updating reservation: {str(e)}")


@csrf_exempt
def delete_reservation(request, reservation_id):
    """
    Deletes a reservation by its ID.

    Args:
        request (HttpRequest): Django HTTP request object
        reservation_id (int): ID of reservation to delete

    Returns:
        JsonResponse: JSON containing a success message
    """
    if request.method != "DELETE":
        return HttpResponseNotAllowed(["DELETE"], "Only DELETE is allowed!")

    try:
        reservation = Reservation.objects.get(id=reservation_id)
        reservation.delete()
        return JsonResponse(
            {"message": f"Reservation {reservation_id} deleted successfully."}, status=204
        )

    except Reservation.DoesNotExist:
        return HttpResponseNotFound("Reservation not found.")
    except Exception as e:
        return HttpResponseServerError(f"Error deleting reservation: {str(e)}")
