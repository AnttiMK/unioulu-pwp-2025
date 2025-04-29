"""
This module contains the views for the REST API.
"""

from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from app.models import User, Table, Reservation, MenuItem, OrderItem, Order
from app.serializers import UserSerializer, ReservationSerializer, TableSerializer, MenuItemSerializer, OrderItemSerializer, OrderSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    Handles requests for the users endpoint.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    search_fields = ['name']

    def perform_create(self, serializer):
        serializer.save()

class TableViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing tables.
    """
    queryset = Table.objects.all()
    serializer_class = TableSerializer

    def perform_create(self, serializer):
        serializer.save()

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        serializer.save()


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
