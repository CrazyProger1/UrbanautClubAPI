from rest_framework import serializers
from abandoned.models import *


class CoordinatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinates
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    city = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    region = serializers.SerializerMethodField()

    class Meta:
        model = Address
        fields = '__all__'

    def get_city(self, obj):
        return obj.city.name

    def get_country(self, obj):
        return obj.country.name

    def get_region(self, obj):
        return obj.city.region.name


class AbandonedObjectLocationSerializer(serializers.ModelSerializer):
    coordinates = CoordinatesSerializer()
    address = AddressSerializer()

    class Meta:
        model = AbandonedObjectLocation
        fields = '__all__'


class AbandonedObjectCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AbandonedObjectCategory
        fields = '__all__'


class AbandonedObjectSerializer(serializers.ModelSerializer):
    location = AbandonedObjectLocationSerializer()

    class Meta:
        model = AbandonedObject
        fields = ('id', 'name', 'description', 'state', 'category', 'location')
