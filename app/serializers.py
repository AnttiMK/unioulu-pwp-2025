from rest_framework import serializers

from app.models import User, Reservation, Table, MenuItem, OrderItem, Order


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name']

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'user', 'table', 'number_of_people', 'date_and_time', 'duration']

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'min_people', 'max_people']

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'type', 'price']


class OrderItemSerializer(serializers.ModelSerializer):
    item_id = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all(), source='item'
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'amount', 'item_id']


class OrderSerializer(serializers.ModelSerializer):
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
