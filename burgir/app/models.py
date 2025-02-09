from django.db import models
from django.core.exceptions import ValidationError


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Table(models.Model):
    min_people = models.IntegerField()
    max_people = models.IntegerField()

    def __str__(self):
        return f"Table {self.id} ({self.min_people}-{self.max_people} people)"


class MenuItem(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=64, unique=True)
    type = models.CharField(max_length=20, default="main course")
    price = models.FloatField()

    def __str__(self):
        return f"{self.name} - {self.description} - {self.price:.2f}€"


class OrderItem(models.Model):
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    amount = models.IntegerField()
    order = models.ForeignKey(
        "Order", on_delete=models.CASCADE, related_name="order_items", null=True
    )

    def __str__(self):
        return f"{self.item} - {self.amount} pcs"


class Order(models.Model):
    status = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")

    def total_price(self):
        return sum(
            (order_item.item.price * order_item.amount)
            for order_item in self.order_items.all()
        )

    def all_items(self):
        return (
            ", ".join(
                f"{order_item.item.name} - {order_item.amount} pcs - {order_item.item.price * order_item.amount} €"
                for order_item in self.order_items.all()
            )
            or "No items"
        )


class Reservation(models.Model):
    number_of_people = models.IntegerField()
    date_and_time = models.DateTimeField()
    duration = models.IntegerField()

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reservations"
    )
    table = models.ForeignKey(
        Table, on_delete=models.CASCADE, related_name="reservations"
    )

    def clean(self):
        """Ensure table capacity is suitable for the reservation"""
        if self.table:
            if self.number_of_people < self.table.min_people:
                raise ValidationError(
                    f"Too few people for this table. Minimum required: {self.table.min_people}."
                )
            if self.number_of_people > self.table.max_people:
                raise ValidationError(
                    f"Too many people for this table. Maximum allowed: {self.table.max_people}."
                )

    def save(self, *args, **kwargs):
        """Run validation before saving the reservation"""
        self.clean()  # Call clean() to validate
        super().save(*args, **kwargs)
