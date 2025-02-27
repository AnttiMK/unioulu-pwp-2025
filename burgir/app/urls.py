from django.urls import include, path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("tables/", views.tables, name="Tables"),
    path("menu/", views.menu, name="Menu Items"),
    # RESERVATIONS
    path("reservations/", views.reservations, name="Reservations"),
    path(
        "reservations/reservation/<int:id>/",
        views.reservation_by_id,
        name="Reservation by id",
    ),
    path(
        "reservations/reservation/<str:user_name>/",
        views.reservations_by_user,
        name="Reservations by user",
    ),
    # ORDERS
    path("orders/", views.orders, name="Orders"),
    path(
        "orders/order/<int:id>/",
        views.order_by_id,
        name="Order by id",
    ),
    path(
        "orders/order/<str:user_name>/",
        views.orders_by_user,
        name="Orders by user",
    ),
]
