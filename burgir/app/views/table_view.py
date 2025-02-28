from ..models import Table
from django.http import JsonResponse


def get_all(request):
    """
    Returns all tables and total number of tables.

    Args:
        _ (HttpRequest): Django HTTP request object (unused)

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
