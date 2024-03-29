import peewee
from database.model import Model
from .limits import *


class Country(Model):
    id = peewee.IntegerField(primary_key=True)
    name = peewee.CharField(max_length=CITY_NAME_LENGTH, unique=True)


class City(Model):
    id = peewee.IntegerField(primary_key=True)
    name = peewee.CharField(max_length=CITY_NAME_LENGTH)
    display_name = peewee.CharField(max_length=CITY_DISPLAY_NAME_LENGTH, unique=True)
    country = peewee.ForeignKeyField(Country)


class Coordinates(Model):
    id = peewee.IntegerField(primary_key=True)
    latitude = peewee.DecimalField(
        max_digits=8,
        decimal_places=5,
        null=True
    )
    longitude = peewee.DecimalField(
        max_digits=8,
        decimal_places=5,
        null=True
    )


class Address(Model):
    id = peewee.IntegerField(primary_key=True)
    # country = peewee.CharField(max_length=100, null=True)
    # city = peewee.CharField(max_length=100, null=True)
    country = peewee.ForeignKeyField(Country)
    city = peewee.ForeignKeyField(City, null=True)
    region = peewee.CharField(max_length=100, null=True)
    street = peewee.CharField(max_length=100, null=True)
    street_number = peewee.CharField(max_length=4, null=True)
    zipcode = peewee.CharField(max_length=10, null=True)


class AbandonedObjectLocation(Model):
    id = peewee.IntegerField(primary_key=True)
    coordinates = peewee.ForeignKeyField(Coordinates)
    address = peewee.ForeignKeyField(Address)


class AbandonedObjectCategory(Model):
    name = peewee.CharField(max_length=50, primary_key=True)


class AbandonedObject(Model):
    id = peewee.IntegerField(primary_key=True)
    name = peewee.CharField(max_length=OBJECT_NAME_LENGTH)
    description = peewee.CharField(max_length=OBJECT_DESCRIPTION_LENGTH)

    # category = peewee.CharField(max_length=50)
    category = peewee.ForeignKeyField(AbandonedObjectCategory, field='name')
    state = peewee.CharField(max_length=1)
    location = peewee.ForeignKeyField(AbandonedObjectLocation)
