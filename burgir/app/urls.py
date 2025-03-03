from django.urls import include, path
from .views import (
    home_view,
    menu_view,
    order_view,
    reservation_view,
    table_view,
    user_view,
)

# django rest framework could make this easier
# https://www.django-rest-framework.org/tutorial/6-viewsets-and-routers/#using-routers

urlpatterns = [
    path("", home_view.home, name="home"),
    # USERS
    path(
        "users/",
        user_view.get_all,
        name="All users",
    ),
    path(
        "users/user/<user_identifier>/",
        user_view.get_by_identifier,
        name="User by id or name",
    ),
    path(
        "users/create/", 
        user_view.create_user, 
        name="Create user"
        ),

    path(
        "users/delete/<int:id>/", 
        user_view.delete_user, 
        name="Delete user"
        ),

    # TABLE
    path(
        "tables/",
        table_view.get_all,
        name="Tables",
    ),
    # MENU
    path(
        "menu/",
        menu_view.get_menu,
        name="Menu Items",
    ),
    path(
        "menu/type/<str:menu_item_type>/",
        menu_view.get_items_by_type,
        name="Get items by type",
    ),
    # RESERVATIONS
    path(
        "reservations/",
        reservation_view.get_all,
        name="All reservations",
    ),
    path(
        "reservations/create/", 
         reservation_view.create_reservation, 
         name="Create reservation"
    ),
    path(
        "reservations/update/<int:id>/", 
         reservation_view.update_reservation, 
         name="Update reservation"
    ),
    path(
        "reservations/delete/<int:id>/", 
         reservation_view.delete_reservation, 
         name="Delete reservation"
    ),
    path(
        "reservations/<str:user_name>/",
        reservation_view.get_by_user,
        name="Reservations by user",
    ),
    path(
        "reservations/reservation/<int:reservation_id>/",
        reservation_view.get_by_id,
        name="Reservation by id",
    ),
    # ORDERS
    path(
        "orders/",
        order_view.get_all,
        name="All orders",
    ),
    path(
        "orders/create/", 
        order_view.create_order, 
        name="Create order"
        ),
    path(
        "orders/update/<int:id>/", 
        order_view.update_order, 
        name="Update order"
        ),
    path(
        "orders/delete/<int:id>/", 
        order_view.delete_order, 
        name="Delete order"),
    path(
        "orders/<str:user_name>/",
        order_view.get_by_user,
        name="Orders by user",
    ),
    path(
        "orders/status/<str:status>/",
        order_view.get_by_status,
        name="Get by status",
    ),
    path(
        "orders/order/<int:order_id>/",
        order_view.get_by_id,
        name="Order by id",
    ),
]
