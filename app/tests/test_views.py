from django.test import TestCase, Client
from django.urls import reverse
from app.models import User, Table, Reservation, MenuItem, Order, OrderItem
from datetime import timedelta


class UserViewSetTest(TestCase):
    # Test case for UserViewSet
    def setUp(self):
        # Set up the test client and create a user
        self.client = Client()
        self.user = User.objects.create(name="Test User")
        self.user_url = reverse('user-detail', args=[self.user.id])

    def test_get_user_list(self):
        # Test case for getting the list of users
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, 200)

    def test_get_user_detail(self):
        # Test case for getting the details of a specific user
        response = self.client.get(self.user_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], self.user.name)

    def test_perform_create(self):
        # Test case for creating a new user
        # Define the endpoint for creating a user
        url = reverse('user-list')  # Adjust if the actual endpoint differs

        # Data to create a new user
        data = {"name": "New Test User"}

        # Send a POST request to create a new user
        response = self.client.post(url, data)

        # Assert that the response status is 201 Created
        self.assertEqual(response.status_code, 201)

        # Assert that the user was created in the database
        self.assertTrue(User.objects.filter(name="New Test User").exists())

        # Assert that the response contains the correct data
        created_user = User.objects.get(name="New Test User")
        self.assertEqual(response.json()['name'], created_user.name)

    def test_get_user_reservations(self):
        # Test case for getting the reservations of a specific user
        table = Table.objects.create(min_people=4, max_people=6)
        reservation = Reservation.objects.create(
            user=self.user, table=table, number_of_people=2, date_and_time="2025-05-15T12:00:00Z", 
            duration=timedelta(hours=2)
        )
        response = self.client.get(f"{self.user_url}reservations/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['id'], reservation.id)

    def test_get_user_orders(self):
        # Test case for getting the orders of a specific user
        order = Order.objects.create(user=self.user, status="Pending")
        response = self.client.get(f"{self.user_url}orders/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['id'], order.id)


class TableViewSetTest(TestCase):
    # Test case for TableViewSet
    def setUp(self):
        # Set up the test client and create a table
        self.client = Client()
        self.table = Table.objects.create(min_people=2, max_people=6)
        self.table_url = reverse('table-detail', args=[self.table.id])

    def test_get_table_list(self):
        # Test case for getting the list of tables
        response = self.client.get(reverse('table-list'))
        self.assertEqual(response.status_code, 200)

    def test_get_table_detail(self):
        # Test case for getting the details of a specific table
        response = self.client.get(self.table_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], self.table.id)

    def test_perform_create(self):
        # Test case for creating a new table
        # Define the endpoint for creating a table
        url = reverse('table-list')  # Adjust if the actual endpoint differs

        # Data to create a new table
        data = {"min_people": 1, "max_people": 2}

        # Send a POST request to create a new table
        response = self.client.post(url, data)

        # Assert that the response status is 201 Created
        self.assertEqual(response.status_code, 201)

        # Assert that the table was created in the database
        self.assertTrue(Table.objects.filter(min_people=1, max_people=2).exists())

        # Assert that the response contains the correct data
        created_table = Table.objects.get(min_people=1, max_people=2)
        self.assertEqual(response.json()['min_people'], created_table.min_people)
        self.assertEqual(response.json()['max_people'], created_table.max_people)


class ReservationViewSetTest(TestCase):
    # Test case for ReservationViewSet
    def setUp(self):
        # Set up the test client and create a reservation
        self.client = Client()
        self.user = User.objects.create(name="Test User")
        self.table = Table.objects.create(min_people=2, max_people=6)
        self.reservation = Reservation.objects.create(
            user=self.user, table=self.table, number_of_people=4, date_and_time="2025-05-15T12:00:00Z", 
            duration=timedelta(hours=2)
        )
        self.reservation_url = reverse('reservation-detail', args=[self.reservation.id])

    def test_get_reservation_list(self):
        # Test case for getting the list of reservations
        response = self.client.get(reverse('reservation-list'))
        self.assertEqual(response.status_code, 200)

    def test_get_reservation_detail(self):
        # Test case for getting the details of a specific reservation
        response = self.client.get(self.reservation_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], self.reservation.id)


class MenuItemViewSetTest(TestCase):
    # Test case for MenuItemViewSet
    def setUp(self):
        # Set up the test client and create a menu item
        self.client = Client()
        self.menu_item = MenuItem.objects.create(name="Pizza", description="Delicious pizza", type="Food", price=10.0)
        self.menu_item_url = reverse('menuitem-detail', args=[self.menu_item.id])

    def test_get_menu_item_list(self):
        # Test case for getting the list of menu items
        response = self.client.get(reverse('menuitem-list'))
        self.assertEqual(response.status_code, 200)

    def test_get_menu_item_detail(self):
        # Test case for getting the details of a specific menu item
        response = self.client.get(self.menu_item_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], self.menu_item.id)


class OrderViewSetTest(TestCase):
    # Test case for OrderViewSet
    def setUp(self):
        # Set up the test client and create an order
        self.client = Client()
        self.user = User.objects.create(name="Test User")
        self.order = Order.objects.create(user=self.user, status="Pending")
        self.order_url = reverse('order-detail', args=[self.order.id])

    def test_get_order_list(self):
        # Test case for getting the list of orders
        response = self.client.get(reverse('order-list'))
        self.assertEqual(response.status_code, 200)

    def test_get_order_detail(self):
        # Test case for getting the details of a specific order
        response = self.client.get(self.order_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], self.order.id)

    def test_perform_create(self):
        # Test case for creating a new order
        # Define the endpoint for creating an order
        url = reverse('order-list')  # Adjust if the actual endpoint differs

        # Create a user for the order
        user = User.objects.create(name="Hungry User")

        # Data to create a new order
        data = {"user_id": user.id, "status": "Preparing"}

        # Send a POST request to create a new order
        response = self.client.post(url, data)

        # Assert that the response status is 201 Created
        self.assertEqual(response.status_code, 201)

        # Assert that the order was created in the database
        self.assertTrue(Order.objects.filter(user=user, status="Preparing").exists())

        # Assert that the response contains the correct data
        created_order = Order.objects.get(user=user, status="Preparing")
        self.assertEqual(response.json()['user_id'], created_order.user.id)
        self.assertEqual(response.json()['status'], created_order.status)


class OrderItemViewSetTest(TestCase):
    # Test case for OrderItemViewSet
    def setUp(self):
        # Set up the test client and create an order item
        self.client = Client()
        self.menu_item = MenuItem.objects.create(name="Pizza", description="Delicious pizza", type="Food", price=10.0)
        self.order = Order.objects.create(user=User.objects.create(name="Test User"), status="Pending")
        self.order_item = OrderItem.objects.create(order=self.order, item=self.menu_item, amount=2)
        self.order_item_url = reverse('orderitem-detail', args=[self.order_item.id])

    def test_get_order_item_list(self):
        # Test case for getting the list of order items
        response = self.client.get(reverse('orderitem-list'))
        self.assertEqual(response.status_code, 200)

    def test_get_order_item_detail(self):
        # Test case for getting the details of a specific order item
        response = self.client.get(self.order_item_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], self.order_item.id)