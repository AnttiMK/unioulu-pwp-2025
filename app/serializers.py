"""
Serializers for the application.
"""
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from app.models import User, Reservation, Table, MenuItem, OrderItem, Order


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    class Meta:
        model = User
        fields = ['id', 'name']

class ReservationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Reservation model.
    """
    class Meta:
        model = Reservation
        fields = ['id', 'user', 'table', 'number_of_people', 'date_and_time', 'duration']

    def create(self, validated_data):
        """
        Override the create method to add custom validation for table availability.
        """
        table = validated_data.get('table')
        date_and_time = validated_data.get('date_and_time')
        duration = validated_data.get('duration')

        # Check that reservation is not in the past
        if date_and_time < timezone.now():
            raise ValidationError("The reservation cannot be in the past.")

        actual_table = Table.objects.get(id=table.id)
        # Check if the number of people is within the table's capacity
        if validated_data.get('number_of_people') < actual_table.min_people \
                or validated_data.get('number_of_people') > actual_table.max_people:
            raise ValidationError("The number of people exceeds the table's capacity.")

        # Check if the table is available
        if not self._is_table_available(table, date_and_time, duration):
            raise ValidationError("The selected table is not available at this time.")

        return super().create(validated_data)

    def _is_table_available(self, table, start_time, duration):
        """
        Checks if a table is available at a given time.

        Args:
            table (Table): The table to check availability for.
            start_time (datetime): The desired reservation start time.
            duration (timedelta): The duration of the reservation.

        Returns:
            bool: True if the table is available, False otherwise.
        """
        end_time = start_time + duration

        # Check if any existing reservation overlaps
        overlapping_reservations = Reservation.objects.filter(
            table=table,
            date_and_time__lt=end_time,
            date_and_time__gt=start_time - duration
        )

        return not overlapping_reservations.exists()

    def update(self, instance, validated_data):
        """
        Override the update method to add custom validation for table availability.
        """
        table = validated_data.get('table', instance.table)
        date_and_time = validated_data.get('date_and_time', instance.date_and_time)
        duration = validated_data.get('duration', instance.duration)

        # Check that reservation is not in the past
        if date_and_time < timezone.now():
            raise ValidationError("The reservation cannot be in the past.")

        actual_table = Table.objects.get(id=table.id)
        # Check if the number of people is within the table's capacity
        if (validated_data.get('number_of_people') < actual_table.min_people \
                or validated_data.get('number_of_people') > actual_table.max_people):
            raise ValidationError("The number of people exceeds the table's capacity.")

        # Check if the table is available
        if not self._is_table_available(table, date_and_time, duration):
            raise ValidationError("The selected table is not available at this time.")

        return super().update(instance, validated_data)


class TableSerializer(serializers.ModelSerializer):
    """
    Serializer for the Table model.
    """
    class Meta:
        model = Table
        fields = ['id', 'min_people', 'max_people']

class MenuItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the MenuItem model.
    """
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'type', 'price']


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the OrderItem model.
    """
    item_id = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all(), source='item'
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'amount', 'item_id']


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model.
    """
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user'
    )

    order_items = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=OrderItem.objects.all()
    )

    class Meta:
        model = Order
        fields = ['id', 'status', 'user_id', 'order_items']
