from datetime import timedelta

from django.core.validators import MinValueValidator
from django.db import models
from django.core.exceptions import ValidationError


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

    def serialize(self, short=False):
        doc = {
            "id": self.id,
            "name": self.name,
        }
        if not short:
            orders = []
            for order in Order.objects.filter(user=self).all():
                orders.append(order.serialize())
            reservations = []
            for reservation in Reservation.objects.filter(user=self).all():
                reservations.append(reservation.serialize())

            doc["orders"] = orders
            doc["reservations"] = reservations

        return doc


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

    def serialize(self):
        return {
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "price": self.price,
        }


class OrderItem(models.Model):
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    amount = models.IntegerField()
    order = models.ForeignKey(
        "Order", on_delete=models.CASCADE, related_name="order_items", null=True
    )

    def __str__(self):
        return f"{self.item} - {self.amount} pcs"

    def serialize(self):
        return {
            "name": self.item.name,
            "amount": self.amount,
            "price": self.item.price,
            "total_price": self.item.price * self.amount,
        }


class Order(models.Model):
    status = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")

    def total_price(self):
        return sum(
            (order_item.item.price * order_item.amount)
            for order_item in self.order_items.all()
        )

    def serialize(self):
        items = []
        for order_item in self.order_items.all():
            items.append(order_item.serialize())

        return {
            "order_num": self.id,
            "status": self.status,
            "user": self.user.name,
            "order_items": items,
            "order_total_price": self.total_price(),
        }

    def all_items(self):
        return (
            ", ".join(
                f"{order_item.item.name} - {order_item.amount} pcs - {order_item.item.price * order_item.amount} €"
                for order_item in self.order_items.all()
            )
            or "No items"
        )


class Reservation(models.Model):
    number_of_people = models.IntegerField(validators=[MinValueValidator(1)])
    date_and_time = models.DateTimeField()
    duration = models.DurationField()

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reservations"
    )
    table = models.ForeignKey(
        Table, on_delete=models.CASCADE, related_name="reservations"
    )

    def serialize(self):
        return {
            "reserver": self.user.name,
            "table": self.table.id,
            "number of people": self.number_of_people,
            "date_and_time": self.date_and_time,
            "duration": self.duration,
        }

    def clean(self):
        """Ensure table capacity is suitable for the reservation"""
        if hasattr(self, "table"):
            if self.number_of_people < self.table.min_people:
                raise ValidationError(
                    f"Too few people for this table. Minimum required: {self.table.min_people}."
                )
            if self.number_of_people > self.table.max_people:
                raise ValidationError(
                    f"Too many people for this table. Maximum allowed: {self.table.max_people}."
                )

            self._ensure_no_overlap()

    def _ensure_no_overlap(self):
        """Ensure that the reservation does not overlap with an existing reservation"""
        end_time = self.date_and_time + self.duration
        overlapping = (
            Reservation.objects.filter(table=self.table)
            .filter(
                date_and_time__lt=end_time,
                date_and_time__gt=self.date_and_time - models.F("duration"),
            )
            .exclude(id=self.id)
        )

        if overlapping.exists():
            raise ValidationError("Reservation overlaps with existing reservations")

    def save(self, *args, **kwargs):
        """Run validation before saving the reservation"""
        self.clean()  # Call clean() to validate
        super().save(*args, **kwargs)
