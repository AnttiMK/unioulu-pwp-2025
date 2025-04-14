"""
This module contains the views for the REST API.
"""

from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from app.models import User, Table
from app.serializers import UserSerializer, ReservationSerializer, TableSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    Handles requests for the users endpoint.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    @action(detail=True, methods=['get'])
    def reservations(self, request, pk=None):
        """
        Returns all reservations for a specific user.
        """
        user = get_object_or_404(User, pk=pk)
        reservations = user.reservations.all()
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)

    @method_decorator(cache_page(60 * 60)) # Cache for 1 hour
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

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
