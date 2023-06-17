from crf.serializer import Serializer
from .models import *


class AbandonedObjectSerializer(Serializer):
    class Meta:
        model = AbandonedObject


class AbandonedObjectLocationSerializer(Serializer):
    class Meta:
        model = AbandonedObjectLocation


class AddressSerializer(Serializer):
    class Meta:
        model = Address


class CoordinatesSerializer(Serializer):
    class Meta:
        model = Coordinates
