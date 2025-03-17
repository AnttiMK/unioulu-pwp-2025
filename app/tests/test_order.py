import json

from django.test import Client
from django.test import TestCase

from ..models import User, MenuItem


class OrderTestCase(TestCase):
    def setUp(self):
        User.objects.create(name="Test User")
        MenuItem.objects.create(
            name="BeeseChurger",
            description="Big burger with cheese",
            price=12.99,
        )

        self.client = Client()

        self.valid_order = {
            "user": "Test User",
            "order_items": [{"item_id": 1, "amount": 3}],
            "status": "preparing",
        }

    def test_create_order_invalid_status(self):
        """Creating an order with an invalid status should fail."""

        request_data = self.valid_order.copy()
        request_data["status"] = "not preparing"

        response = self.client.post(
            "/orders/create/",
            json.dumps(request_data),
            content_type="application/json",
        )

        self.assertNotEqual(
            response.status_code, 201, "Created order with invalid status!"
        )
