"""Tests for the reservation API"""
import json
from datetime import datetime, timedelta

from django.test import Client
from django.test import TestCase
from django.utils import timezone

from ..models import User, Table, Reservation


# Create your tests here.
class ReservationTestCase(TestCase):
    """Tests for the reservation API"""
    def setUp(self):
        self.user = User.objects.create(name="Test User")
        self.table = Table.objects.create(min_people=2, max_people=4)

        # create reservations in the db for get
        for i in range(-1, 2):
            time = timezone.now() + i * timedelta(days=1)
            Reservation.objects.create(
                user=self.user,
                table=self.table,
                number_of_people=3,
                date_and_time=time,
                duration=timedelta(hours=2),
            )

        self.client = Client()

        self.valid_time = (timezone.now() + timedelta(days=2)).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # valid reservation base
        self.valid_reservation = {
            "reserver": "Test User",
            "table": self.table.id,
            "number_of_people": self.table.min_people,
            "date_and_time": self.valid_time,
            "duration": "02:00:00",
        }

    def test_create_valid(self):
        """Making a reservation with valid values should return 201"""
        response = self.client.post(
            "/reservations/create/",
            json.dumps(self.valid_reservation),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201, "Making reservation failed!")

    def test_create_overlapping(self):
        """Making an overlapping reservation should return 400."""
        # post the same reservation twice
        self.client.post(
            "/reservations/create/",
            json.dumps(self.valid_reservation),
            content_type="application/json",
        )
        response = self.client.post(
            "/reservations/create/",
            json.dumps(self.valid_reservation),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400, "Made overlapping reservation!")

    def test_create_past_reservation(self):
        """Making a reservation in the past should return 400."""
        past_time = (timezone.now() - timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S")

        request_data = self.valid_reservation.copy()
        request_data["date_and_time"] = past_time

        response = self.client.post(
            "/reservations/create/",
            json.dumps(request_data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400, "Made reservation in the past!")

    def test_create_reservation_people_min(self):
        """Making a reservation with too few people should return 400"""

        request_data = self.valid_reservation.copy()
        request_data["number_of_people"] = 1

        response = self.client.post(
            "/reservations/create/",
            json.dumps(request_data),
            content_type="application/json",
        )

        self.assertEqual(
            response.status_code, 400, "Made reservation with too few people!"
        )

    def test_create_reservation_people_max(self):
        """Making a reservation with too many people should return 400"""

        request_data = self.valid_reservation.copy()
        request_data["number_of_people"] = 5

        response = self.client.post(
            "/reservations/create/",
            json.dumps(request_data),
            content_type="application/json",
        )
        response = self.client.post(
            "/reservations/create/",
            json.dumps(request_data),
            content_type="application/json",
        )
        self.assertEqual(
            response.status_code, 400, "Made reservation with too many people!"
        )

    def test_get_by_time_upcoming(self):
        """Test getting upcoming reservations"""

        response = self.client.get("/reservations/status/upcoming/")

        reservations = json.loads(response.content)["reservations"]
        self.assertEqual(len(reservations), 1, "Returned more than one reservation!")

        time = datetime.strptime(reservations[0]["date_and_time"], "%Y-%m-%d %H:%M:%S")

        self.assertGreater(time, datetime.now())

    def test_get_by_time_current(self):
        """Test getting current reservations"""

        response = self.client.get("/reservations/status/current/")

        reservations = json.loads(response.content)["reservations"]
        self.assertEqual(len(reservations), 1, "Returned more than one reservation!")

        time = datetime.strptime(reservations[0]["date_and_time"], "%Y-%m-%d %H:%M:%S")

        hours, minutes, seconds = map(int, reservations[0]["duration"].split(":"))
        duration = timedelta(hours=hours, minutes=minutes, seconds=seconds)

        # subtract 30 seconds from current time, as the starting time is current time
        self.assertGreater(time, (datetime.now() - timedelta(seconds=30)))
        self.assertLess(datetime.now(), time + duration)

    def test_get_by_time_past(self):
        """Test getting past reservations"""

        response = self.client.get("/reservations/status/past/")

        reservations = json.loads(response.content)["reservations"]
        time = datetime.strptime(reservations[0]["date_and_time"], "%Y-%m-%d %H:%M:%S")

        hours, minutes, seconds = map(int, reservations[0]["duration"].split(":"))
        duration = timedelta(hours=hours, minutes=minutes, seconds=seconds)

        self.assertLess(time + duration, datetime.now())

    def test_get_by_time_invalid(self):
        """Using invalid status as query should return 400"""

        response = self.client.get("/reservations/status/invalid/")

        self.assertEqual(
            response.status_code, 400, "Statuscode for invalid request was not 400!"
        )
