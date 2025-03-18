import json
from django.test import TestCase, Client
from django.urls import reverse
from ..models import User

class UserViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create(name="Alice")
        self.user2 = User.objects.create(name="Bob")

    def test_get_all_users(self):
        response = self.client.get(reverse("All users"))
        self.assertEqual(response.status_code, 200)
        self.assertIn('user_count', response.json())
        self.assertEqual(response.json()['user_count'], 2)

    def test_get_all_users_invalid_method(self):
        response = self.client.post(reverse("All users"))
        self.assertEqual(response.status_code, 405)

    def test_get_user_by_identifier(self):
        response = self.client.get(reverse("User by id or name", args=[self.user1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn('name', response.json())
        self.assertEqual(response.json()['name'], "Alice")

    def test_get_user_by_identifier_not_found(self):
        response = self.client.get(reverse("User by id or name", args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_get_user_by_identifier_invalid_method(self):
        response = self.client.post(reverse("User by id or name", args=[self.user1.id]))
        self.assertEqual(response.status_code, 405)

    def test_create_user(self):
        data = {
            "name": "Charlie"
        }
        response = self.client.post(reverse("Create user"), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn('name', response.json())
        self.assertEqual(response.json()['name'], "Charlie")

    def test_create_user_identical_name(self):
        # Attempt to create a user with the same name as an existing user should fail
        data = {
            "name": "Alice"
        }
        response = self.client.post(reverse("Create user"), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_create_user_missing_fields(self):
        data = {}
        response = self.client.post(reverse("Create user"), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_create_user_invalid_json(self):
        response = self.client.post(reverse("Create user"), "invalid json", content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_get_create_user(self):
        response = self.client.get(reverse("Create user"))
        self.assertEqual(response.status_code, 405)

    def test_delete_user(self):
        response = self.client.delete(reverse("Delete user", args=[self.user1.id]))
        self.assertEqual(response.status_code, 200)

    def test_delete_user_not_found(self):
        response = self.client.delete(reverse("Delete user", args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_delete_user_invalid_method(self):
        response = self.client.put(reverse("Delete user", args=[self.user1.id]))
        self.assertEqual(response.status_code, 405)