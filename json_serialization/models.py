# -*- coding: utf-8 -*-


class User(object):
    #Include these fields if you want defaults
    name = ""
    dob = None
    is_employee = False

    def __init__(self, name, dob, is_employee):
        self.name = name
        self.dob = dob
        self.is_employee = is_employee


class Dealership(object):
    #Include these fields if you want defaults
    name = ""
    location = None

    def __init__(self, name, location):
        self.name = name
        self.location = location

    def sell_vehicle(self, vehicle, sales_person, new_owner):
        if not sales_person.is_employee:
            raise Exception("Vehicles can only be sold by employees")
        vehicle.owner = new_owner


class Vehicle(object):
    #Include these fields if you want defaults
    name = ""
    year = None
    make = None
    vehicle_type = None
    owner = None

    def __init__(self, name, year, make, vehicle_type, owner):
        self.name = name
        self.year = year
        self.make = make
        self.vehicle_type = vehicle_type
        self.owner = owner
