from rest_framework import serializers, relations
from abandoned.models import *
from abandoned.services import *


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

    def create(self, validated_data):
        coordinates_data = validated_data.pop('coordinates')
        address_data = validated_data.pop('address')

        coordinates = CoordinatesSerializer().create(coordinates_data)
        address = AddressSerializer().create(address_data)

        return AbandonedObjectLocation.objects.create(coordinates=coordinates, address=address)


class AbandonedObjectCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AbandonedObjectCategory
        fields = '__all__'


class AbandonedObjectSerializer(serializers.ModelSerializer):
    location = AbandonedObjectLocationSerializer()

    class Meta:
        model = AbandonedObject
        fields = ('id', 'name', 'description', 'state', 'category', 'location')

    def create(self, validated_data):
        location_data = validated_data.pop('location')
        location = AbandonedObjectLocationSerializer().create(location_data)
        return AbandonedObject.objects.create(**validated_data, location=location)
