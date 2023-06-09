import cities_light
from django.core import validators
from django.db import models
from abandoned.limits import *


# from django.contrib.gis.db import models


class AbandonedObjectState(models.TextChoices):
    DANGEROUS = 'd', 'dangerous'
    BAD = 'b', 'bad'
    AVERAGE = 'a', 'average'
    GOOD = 'g', 'good'
    NOVELTY = 'n', 'novelty'


class AbandonedObjectCategory(models.Model):
    class Meta:
        verbose_name = 'AbandonedObjectCategory'
        verbose_name_plural = 'AbandonedObjectCategories'

    name = models.CharField(max_length=CATEGORY_NAME_LENGTH, primary_key=True)


class Coordinates(models.Model):
    class Meta:
        unique_together = ('latitude', 'longitude')
        verbose_name = 'Coordinates'
        verbose_name_plural = 'Coordinates'

    id = models.AutoField(primary_key=True)
    latitude = models.DecimalField(
        max_digits=8,
        decimal_places=5,
        null=True,
        blank=True
    )
    longitude = models.DecimalField(
        max_digits=8,
        decimal_places=5,
        null=True,
        blank=True
    )


class Address(models.Model):
    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    id = models.AutoField(primary_key=True)
    country = models.ForeignKey('cities_light.Country', on_delete=models.CASCADE, null=False)
    city = models.ForeignKey('cities_light.City', on_delete=models.CASCADE, null=False)
    street = models.CharField(max_length=STREET_NAME_LENGTH, null=True, default=None)
    street_number = models.CharField(max_length=4, null=True, default=None)
    zipcode = models.CharField(max_length=10, null=True, default=None)


class AbandonedObjectLocation(models.Model):
    class Meta:
        verbose_name = 'AbandonedObjectLocation'
        verbose_name_plural = 'AbandonedObjectLocations'

    coordinates = models.ForeignKey(
        to=Coordinates,
        on_delete=models.CASCADE,
        null=False
    )
    address = models.ForeignKey(
        to=Address,
        on_delete=models.SET_NULL,
        null=True
    )


class AbandonedObject(models.Model):
    class Meta:
        verbose_name = 'AbandonedObject'
        verbose_name_plural = 'AbandonedObjects'

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=ABANDONED_OBJECT_NAME_LENGTH, null=False)
    description = models.CharField(max_length=ABANDONED_OBJECT_DESC_LENGTH, null=False)
    hidden = models.BooleanField(default=False)
    category = models.ForeignKey(
        to=AbandonedObjectCategory,
        on_delete=models.SET_NULL,
        null=True
    )
    state = models.CharField(
        max_length=1,
        choices=AbandonedObjectState.choices,
        default=AbandonedObjectState.AVERAGE,
        null=False
    )
    location = models.ForeignKey(
        to=AbandonedObjectLocation,
        on_delete=models.CASCADE,
        null=False
    )
