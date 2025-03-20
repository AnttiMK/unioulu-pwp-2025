from django.urls import path
from .views import (
    home_view,
    menu_view,
    order_view,
    reservation_view,
    table_view,
    user_view,
)

urlpatterns = [
    path("", home_view.home, name="home"),
    # USERS
    path(
        "users/",
        user_view.user,
        name="Users",
    ),
    path(
        "users/<user_identifier>/",
        user_view.user_id,
        name="UsersID",
    ),
    # TABLE
    path(
        "tables/",
        table_view.tables,
        name="Tables",
    ),
    # MENU
    path(
        "menu/",
        menu_view.menu,
        name="Menu Items",
    ),
    path(
        "menu/<str:menu_item_type>/",
        menu_view.get_items_by_type,
        name="Get items by type",
    ),
    # RESERVATIONS
    path(
        "reservations/",
        reservation_view.reservations,
        name="Reservations",
    ),
    path(
        "reservations/<reservation_identifier>/",
        reservation_view.reservation_id,
        name="ReservationsID",
    ),
    # ORDERS
    path(
        "orders/",
        order_view.orders,
        name="Orders",
    ),
    path(
        "orders/<order_identifier>/",
        order_view.orders_id,
        name="OrdersID",
    ),
]
