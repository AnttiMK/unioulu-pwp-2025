"""Models for the application."""
from django.core.validators import MinValueValidator
from django.db import models


class User(models.Model):
    """Represents a user/client that can make orders and reservations."""
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Table(models.Model):
    """Represents a table in the restaurant."""
    min_people = models.IntegerField()
    max_people = models.IntegerField()

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"Table {self.id} ({self.min_people}-{self.max_people} people)"


class MenuItem(models.Model):
    """Represents a menu item that can be ordered."""
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=255)  # Increased max_length to be more realistic
    type = models.CharField(max_length=20, default="main course")
    price = models.FloatField()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} (${self.price})"


class Order(models.Model):
    """Represents an order made by a user."""
    status = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"Order {self.id} by {self.user.name}"


class OrderItem(models.Model):
    """Represents an item in an order."""
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    amount = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.amount}x {self.item.name}"


class Reservation(models.Model):
    """Represents a table reservation made by a user."""
    number_of_people = models.IntegerField(validators=[MinValueValidator(1)])
    date_and_time = models.DateTimeField()
    duration = models.DurationField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reservations")
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name="reservations")

    class Meta:
        ordering = ["date_and_time"]

    def __str__(self):
        return f"Reservation by {self.user.name} on {self.date_and_time.strftime('%Y-%m-%d %H:%M')}"
