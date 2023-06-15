from django_filters import rest_framework as filters
from abandoned.models import AbandonedObject


class AbandonedObjectFilter(filters.FilterSet):
    class Meta:
        model = AbandonedObject
        fields = ('name', 'category', 'state')
