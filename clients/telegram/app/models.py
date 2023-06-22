import peewee
from database.model import Model


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
    country = peewee.CharField(max_length=100, null=True)
    city = peewee.CharField(max_length=100, null=True)
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
    name = peewee.CharField(max_length=250)
    description = peewee.CharField(max_length=100)

    category = peewee.CharField(max_length=50)
    # category = peewee.ForeignKeyField(AbandonedObjectCategory, field='name')
    state = peewee.CharField(max_length=1)
    location = peewee.ForeignKeyField(AbandonedObjectLocation)
