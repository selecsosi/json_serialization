#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import datetime
import unittest
import json
from ..models import User, Vehicle, Dealership
from ..serialization import ModelEncoder, decode_user, decode_vehicle, decode_dealership


class TestSerialization(unittest.TestCase):

    def setUp(self):
        # Create some sample data
        buyer_dob = datetime.datetime(1999, 1, 5)
        salesperson_dob = datetime.datetime(1978, 5, 14)
        self.buyer = User("Steve McStephenson", buyer_dob, False)
        self.salesperson = User("Bill Wiseguy", salesperson_dob, True)
        self.used_jeep = Vehicle(
            "Sweet Jeep",
            1999,
            "Jeep",
            "SUV",
            self.salesperson
        )
        self.dealership = Dealership(
            "Bills Chevy Dealership",
            (41.878247, -87.629767)
        )

    def test_selling_a_cars(self):
        self.dealership.sell_vehicle(self.used_jeep, self.salesperson, self.buyer)
        self.assertEquals(self.used_jeep.owner, self.buyer)

    def test_user_serialization(self):
        encoder = ModelEncoder()
        user_string = json.dumps(self.buyer, default=encoder.default)
        expected = '{"dob": "1999-01-05T00:00:00", "is_employee": false, "name": "Steve McStephenson"}'
        self.assertEqual(user_string, expected)

    def test_vehicle_serialization(self):
        encoder = ModelEncoder()
        vehicle_string = json.dumps(self.used_jeep, default=encoder.default)
        expected = '{"owner": {"dob": "1978-05-14T00:00:00", "is_employee": true, "name": "Bill Wiseguy"}, "make": "Jeep", "vehicle_type": "SUV", "name": "Sweet Jeep", "year": 1999}'
        self.assertEqual(vehicle_string, expected)

    def test_dealership_serialization(self):
        encoder = ModelEncoder()
        dealership_string = json.dumps(self.dealership, default=encoder.default)
        expected = '{"location_lon": -87.629767, "name": "Bills Chevy Dealership", "location_lat": 41.878247}'
        self.assertEqual(dealership_string, expected)

    def test_user_deserialization(self):
        user_string = '{"dob": "1999-01-05T00:00:00", "is_employee": false, "name": "Steve McStephenson"}'
        user = json.loads(user_string, object_hook=decode_user)
        self.assertEquals(user.dob, datetime.datetime(1999, 1, 5))
        self.assertFalse(user.is_employee)
        self.assertEquals(user.name, "Steve McStephenson")

    def test_vehicle_deserialization(self):
        vehicle_string = '{"owner": {"dob": "1978-05-14T00:00:00", "is_employee": true, "name": "Bill Wiseguy"}, "make": "Jeep", "vehicle_type": "SUV", "name": "Sweet Jeep", "year": 1999}'
        vehicle = json.loads(vehicle_string, object_hook=decode_vehicle)
        self.assertEquals(vehicle.name, "Sweet Jeep")
        self.assertEquals(vehicle.year, 1999)
        self.assertEquals(vehicle.owner.name, "Bill Wiseguy")
        self.assertEquals(vehicle.owner.dob, datetime.datetime(1978, 5, 14))

    def test_dealership_deserialization(self):
        dealership_string = '{"location_lon": -87.629767, "name": "Bills Chevy Dealership", "location_lat": 41.878247}'
        dealership = json.loads(dealership_string, object_hook=decode_dealership)
        self.assertEquals(dealership.name, "Bills Chevy Dealership")
        self.assertIsNotNone(dealership.location)
        self.assertEquals(dealership.location, (41.878247, -87.629767))


if __name__ == '__main__':
    unittest.main()
