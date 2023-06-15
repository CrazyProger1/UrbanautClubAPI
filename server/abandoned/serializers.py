from rest_framework import serializers
from abandoned.models import *


class AbandonedObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbandonedObject
        fields = '__all__'
