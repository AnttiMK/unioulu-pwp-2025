from ..models import Table
from django.http import HttpResponseNotAllowed, JsonResponse


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


def create_table(request, id):
    pass


def update_table(request, id):
    pass


def delete_table(request, id):
    pass
