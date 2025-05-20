"""
This module contains the views for the REST API.
"""
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from app.models import User, Table, Reservation, MenuItem, OrderItem, Order
from app.serializers import UserSerializer, ReservationSerializer, TableSerializer, MenuItemSerializer, \
    OrderItemSerializer, OrderSerializer


@extend_schema_view(
    list=extend_schema(summary="List users", description="Retrieve a paginated list of all users.",
                       responses={200: UserSerializer}),
    create=extend_schema(summary="Create user", description="Create a new user with the provided information.",
                         request=UserSerializer, responses={201: UserSerializer, 400: None}),
    retrieve=extend_schema(summary="Retrieve user", description="Get details of a specific user by ID.",
                           responses={200: UserSerializer, 404: None}),
    update=extend_schema(summary="Update user", description="Update all fields of a user.",
                         request=UserSerializer, responses={200: UserSerializer, 400: None, 404: None}),
    partial_update=extend_schema(summary="Partially update user", description="Update one or more fields of a user.",
                                 request=UserSerializer, responses={200: UserSerializer, 400: None, 404: None}),
    destroy=extend_schema(summary="Delete user", description="Delete a user by ID.", responses={204: None, 404: None}),
    reservations=extend_schema(summary="List user reservations", description="Retrieve all reservations for a specific user.",
                               responses={200: ReservationSerializer}),
    orders=extend_schema(summary="List user orders", description="Retrieve all orders for a specific user.",
                         responses={200: OrderSerializer}))
class UserViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    search_fields = ['name']

    @action(detail=True, methods=['get'])
    # pylint: disable=unused-argument
    def reservations(self, request, pk=None):
        """
        Retrieve all reservations for a specific user.
        """
        user = self.get_object()
        reservations = user.reservations.all()
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    # pylint: disable=unused-argument
    def orders(self, request, pk=None):
        """
        Retrieve all orders for a specific user.
        """
        user = self.get_object()
        orders = user.orders.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save()


@extend_schema_view(
    list=extend_schema(summary="List tables", description="Retrieve a paginated list of all tables.",
                       responses={200: TableSerializer}),
    create=extend_schema(summary="Create table",
                         description="Create a new table with the provided details.",
                         request=TableSerializer,
                         responses={201: TableSerializer,400: None}),
    retrieve=extend_schema(summary="Retrieve table",
                           description="Get details of a specific table by ID.",
                           responses={200: TableSerializer, 404: None}),
    update=extend_schema(summary="Update table", description="Update all fields of a table.",
                         request=TableSerializer,
                         responses={200: TableSerializer, 400: None, 404: None}),
    partial_update=extend_schema(summary="Partially update table",
                                 description="Update one or more fields of a table.",
                                 request=TableSerializer, responses={200: TableSerializer, 400: None, 404: None}),
    destroy=extend_schema(summary="Delete table", description="Delete a table by ID.",
                          responses={204: None, 404: None}),
    reservations=extend_schema(summary="List table reservations",
                               description="Retrieve all reservations for a specific table.",
                               responses={200: ReservationSerializer})
)
class TableViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing tables.
    """
    queryset = Table.objects.all()
    serializer_class = TableSerializer

    @action(detail=True, methods=['get'])
    # pylint: disable=unused-argument
    def reservations(self, request, pk=None):
        """
        Retrieve all reservations for a specific table.
        """
        table = self.get_object()
        reservations = table.reservations.all()
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save()


@extend_schema_view(
    list=extend_schema(summary="List reservations", description="Retrieve a paginated list of all reservations.",
                       responses={200: ReservationSerializer}),
    create=extend_schema(summary="Create reservation",
                         description="Create a new reservation with the provided details.",
                         request=ReservationSerializer,
                         responses={201: ReservationSerializer,400: None}),
    retrieve=extend_schema(summary="Retrieve reservation", description="Get details of a specific reservation by ID.",
                           responses={200: ReservationSerializer, 404: None}),
    update=extend_schema(summary="Update reservation", description="Update all fields of a reservation.",
                         request=ReservationSerializer, responses={200: ReservationSerializer, 400: None, 404: None}),
    partial_update=extend_schema(summary="Partially update reservation",
                                 description="Update one or more fields of a reservation.",
                                 request=ReservationSerializer,
                                 responses={200: ReservationSerializer, 400: None, 404: None}),
    destroy=extend_schema(summary="Delete reservation", description="Delete a reservation by ID.",
                          responses={204: None, 404: None}))
class ReservationViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing reservations.
    """
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


@extend_schema_view(
    list=extend_schema(summary="List menu items", description="Retrieve a paginated list of all menu items.",
                       responses={200: MenuItemSerializer}),
    create=extend_schema(summary="Create menu item", description="Create a new menu item with the provided details.",
                         request=MenuItemSerializer, responses={201: MenuItemSerializer, 400: None}),
    retrieve=extend_schema(summary="Retrieve menu item", description="Get details of a specific menu item by ID.",
                           responses={200: MenuItemSerializer, 404: None}),
    update=extend_schema(summary="Update menu item", description="Update all fields of a menu item.",
                         request=MenuItemSerializer, responses={200: MenuItemSerializer, 400: None, 404: None}),
    partial_update=extend_schema(summary="Partially update menu item",
                                 description="Update one or more fields of a menu item.", request=MenuItemSerializer,
                                 responses={200: MenuItemSerializer, 400: None, 404: None}),
    destroy=extend_schema(summary="Delete menu item", description="Delete a menu item by ID.",
                          responses={204: None, 404: None}))
class MenuItemViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing menu items.
    """
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


@extend_schema_view(
    list=extend_schema(summary="List orders", description="Retrieve a paginated list of all orders.",
                       responses={200: OrderSerializer}),
    create=extend_schema(summary="Create order",
                         description="Create a new order with the provided details.",
                         request=OrderSerializer, responses={201: OrderSerializer, 400: None}),
    retrieve=extend_schema(summary="Retrieve order",
                           description="Get details of a specific order by ID.",
                           responses={200: OrderSerializer, 404: None}),
    update=extend_schema(summary="Update order", description="Update all fields of an order.",
                         request=OrderSerializer,
                         responses={200: OrderSerializer, 400: None, 404: None}),
    partial_update=extend_schema(summary="Partially update order",
                                 description="Update one or more fields of an order.",
                                 request=OrderSerializer,
                                 responses={200: OrderSerializer, 400: None, 404: None}),
    destroy=extend_schema(summary="Delete order", description="Delete an order by ID.",
                          responses={204: None, 404: None}))
class OrderViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing orders.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        serializer.save()


@extend_schema_view(
    list=extend_schema(summary="List order items", description="Retrieve a paginated list of all order items.",
                       responses={200: OrderItemSerializer}),
    create=extend_schema(summary="Create order item", description="Create a new order item with the provided details.",
                         request=OrderItemSerializer, responses={201: OrderItemSerializer, 400: None}),
    retrieve=extend_schema(summary="Retrieve order item", description="Get details of a specific order item by ID.",
                           responses={200: OrderItemSerializer, 404: None}),
    update=extend_schema(summary="Update order item", description="Update all fields of an order item.",
                         request=OrderItemSerializer, responses={200: OrderItemSerializer, 400: None, 404: None}),
    partial_update=extend_schema(summary="Partially update order item",
                                 description="Update one or more fields of an order item.", request=OrderItemSerializer,
                                 responses={200: OrderItemSerializer, 400: None, 404: None}),
    destroy=extend_schema(summary="Delete order item", description="Delete an order item by ID.",
                          responses={204: None, 404: None}))
class OrderItemViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing order items.
    """
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
