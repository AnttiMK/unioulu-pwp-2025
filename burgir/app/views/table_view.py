from ..models import Table
from django.http import (
    JsonResponse,
    HttpResponseNotFound,
    HttpResponseBadRequest,
    HttpResponseNotAllowed,
    HttpResponseServerError,
    HttpResponse
)
import json


def get_all(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"], "Only GET is allowed!")
    """
    Returns all tables and total number of tables.

    Args:
        _ (HttpRequest): Django HTTP request object

    Returns:
        JsonResponse: JSON containing all the tables

    """
    tables = {"table_count": 0, "tables": []}
    for table in Table.objects.all():
        tables["table_count"] += 1
        tables["tables"].append(table.serialize())
    return JsonResponse(tables)


def create_table(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Only POST is allowed.")

    try:
        data = json.loads(request.body)
        min_people = data.get("min_people")
        max_people = data.get("max_people")

        if min_people is None or max_people is None:
            return HttpResponseBadRequest("Missing required fields: 'min_people' and 'max_people'.")

        new_table = Table.objects.create(min_people=min_people, max_people=max_people)
        return JsonResponse(new_table.serialize(), status=201)

    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON format.")
    except Exception as e:
        return HttpResponseServerError(f"Error creating table: {str(e)}")


def update_table(request, id):
    pass


def delete_table(request, id):
    pass
