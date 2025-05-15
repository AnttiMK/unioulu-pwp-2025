from django.test import TestCase, Client
from django.urls import reverse
from app.models import User, Table, Reservation, MenuItem, Order, OrderItem
from datetime import timedelta, datetime

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(name="Test User")

    def test_user_str_method(self):
        # Test case for the __str__ method of the User model
        self.assertEqual(str(self.user), "Test User")

class TableModelTest(TestCase):
    def setUp(self):
        self.table = Table.objects.create(min_people=2, max_people=6)

    def test_table_str_method(self):
        # Test case for the __str__ method of the Table model
        self.assertEqual(str(self.table), "Table 1 (2-6 people)")

class MenuItemModelTest(TestCase):
    def setUp(self):
        self.menu_item = MenuItem.objects.create(
            name="Pasta Carbonara",
            description="Classic Italian pasta with creamy sauce",
            type="main course",
            price=12.99
        )

    def test_menu_item_str_method(self):
        # Test case for the __str__ method of the MenuItem model
        self.assertEqual(str(self.menu_item), "Pasta Carbonara ($12.99)")

class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(name="Test User")
        self.order = Order.objects.create(user=self.user, status="Pending")

    def test_order_str_method(self):
        # Test case for the __str__ method of the Order model
        self.assertEqual(str(self.order), "Order 1 by Test User")

class OrderItemModelTest(TestCase):
    def setUp(self):
        self.menu_item = MenuItem.objects.create(
            name="Pasta Carbonara",
            description="Classic Italian pasta with creamy sauce",
            type="main course",
            price=12.99
        )
        self.order_item = OrderItem.objects.create(item=self.menu_item, amount=2, order=None)

    def test_order_item_str_method(self):
        # Test case for the __str__ method of the OrderItem model
        self.assertEqual(str(self.order_item), "2x Pasta Carbonara")

class ReservationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(name="John Doe")
        self.table = Table.objects.create(min_people=2, max_people=6)
        self.reservation = Reservation.objects.create(
            number_of_people=4,
            date_and_time=datetime(2025, 5, 20, 18, 30),
            duration=timedelta(hours=2),
            user=self.user,
            table=self.table
        )

    def test_reservation_str_method(self):
        # Test case for the __str__ method of the Reservation model
        self.assertEqual(
            str(self.reservation),
            "Reservation by John Doe on 2025-05-20 18:30"
        )