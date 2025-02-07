from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("tables/", views.tables, name="Tables"),
    path("menu/", views.menu, name="Menu Items"),
    path("reservations/", views.reservations, name="Reservations"),
    path("orders/", views.orders, name="Orders")
]
