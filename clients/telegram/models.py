import peewee
from crf import Model, Serializer


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
    # country = models.ForeignKey('cities_light.Country', on_delete=models.CASCADE)
    # city = models.ForeignKey('cities_light.City', on_delete=models.CASCADE)
    street = peewee.CharField(max_length=100, null=True)
    street_number = peewee.CharField(max_length=4, null=True)
    zipcode = peewee.CharField(max_length=10, null=True)


class AbandonedObjectLocation(Model):
    id = peewee.IntegerField(primary_key=True)
    coordinates = peewee.ForeignKeyField(Coordinates)
    address = peewee.ForeignKeyField(Address)


class AbandonedObject(Model):
    id = peewee.IntegerField(primary_key=True)
    name = peewee.CharField(max_length=250)
    description = peewee.CharField(max_length=100)

    category = peewee.CharField(max_length=50)
    state = peewee.CharField(max_length=1)
