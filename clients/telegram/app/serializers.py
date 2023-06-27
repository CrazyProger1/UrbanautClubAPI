from crf.serializer import Serializer, MethodField
from .models import *


class AbandonedObjectSerializer(Serializer):
    class Meta:
        model = AbandonedObject


class AbandonedObjectCategorySerializer(Serializer):
    class Meta:
        model = AbandonedObjectCategory


class AbandonedObjectLocationSerializer(Serializer):
    class Meta:
        model = AbandonedObjectLocation


class AddressSerializer(Serializer):
    class Meta:
        model = Address


class CoordinatesSerializer(Serializer):
    class Meta:
        model = Coordinates


class CitySerializer(Serializer):
    country = MethodField(setter='set_country')

    class Meta:
        model = City

    @classmethod
    def set_country(cls, data: dict, ):
        data['country'] = int(data['country'].split('/')[-2])


class CountrySerializer(Serializer):
    class Meta:
        model = Country
