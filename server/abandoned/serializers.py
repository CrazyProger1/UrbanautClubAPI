from rest_framework import serializers
from abandoned.models import *


class CoordinatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinates
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class AbandonedObjectLocationSerializer(serializers.ModelSerializer):
    coordinates = CoordinatesSerializer()
    address = AddressSerializer()

    class Meta:
        model = AbandonedObjectLocation
        fields = '__all__'


class AbandonedObjectSerializer(serializers.ModelSerializer):
    location = AbandonedObjectLocationSerializer()

    class Meta:
        model = AbandonedObject
        fields = ('id', 'name', 'description', 'state', 'category', 'location')
