from rest_framework import serializers

from app.models import User, Reservation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name']

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'user', 'table', 'number_of_people', 'date_and_time', 'duration']
