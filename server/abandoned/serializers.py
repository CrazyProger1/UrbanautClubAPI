from rest_framework import serializers
from abandoned.models import *


class AbandonedObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbandonedObject
        fields = ('id', 'name', 'description', 'state', 'category', 'location')
