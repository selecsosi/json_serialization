# -*- coding: utf-8 -*-
import json
import dateutil.parser
import pytz
from .models import Dealership, Vehicle, User


class ModelEncoder(json.JSONEncoder):
    encoders = {
        'User': 'encode_user',
        'Dealership': 'encode_dealership',
        'Vehicle': 'encode_vehicle',
    }

    def default(self, o):
        """
        This method is the hook for the json serializer to know what method to
        call for each type of model
        """
        encoder_name = self.encoders.get(o.__class__.__name__)
        if encoder_name is None:
            super(ModelEncoder, self).default(o)
        encoder = getattr(self, encoder_name)
        return encoder(o)

    def encode_user(self, user):
        return {
            "name": user.name,
            "dob": user.dob.isoformat() if user.dob else None,
            "is_employee": user.is_employee,
        }

    def encode_dealership(self, dealership):
        return {
            "name": dealership.name,
            "location_lat": dealership.location[0] if dealership.location else None,
            "location_lon": dealership.location[1] if dealership.location else None,
        }

    def encode_vehicle(self, vehicle):
        return {
            "name": vehicle.name,
            "year": vehicle.year,
            "make": vehicle.make,
            "vehicle_type": vehicle.vehicle_type,
            "owner": self.encode_user(vehicle.owner)
        }


"""
Helper methods for deserialization
"""


def decode_user(user_dict):
    return User(
        user_dict["name"],
        convert_iso_stamp(user_dict["dob"]),
        user_dict["is_employee"]
    )


def decode_dealership(dealership_dict):
    return Dealership(
        dealership_dict["name"],
        (dealership_dict["location_lat"], dealership_dict["location_lon"])
    )


def decode_vehicle(vehicle_dict):
    # This will get called for every object starting with the most nested
    # Pick a field that is unique to the top level object so that it can know when
    # to stop. We can talk about this case, which is kind of a pain somewhat.
    # For nested objects I might recommend writing a full class to manage decoding
    if vehicle_dict.get("year", None):
        return Vehicle(
            vehicle_dict["name"],
            vehicle_dict["year"],
            vehicle_dict["make"],
            vehicle_dict["vehicle_type"],
            decode_user(vehicle_dict["owner"])
        )
    else:
        # Return the object and keep moving up the object tree
        return vehicle_dict


def convert_iso_stamp(t, tz=None):
    """
    Helper method for some timestamp conversion
    """
    if t is None:
        return None

    dt = dateutil.parser.parse(t)
    if tz is not None:
        timezone = pytz.timezone(tz)
        if dt.tzinfo is None:
            dt = timezone.localize(dt)
    return dt
