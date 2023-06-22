from rest_framework import generics
from abandoned.serializers import *
from abandoned.services import *
from abandoned.filters import *
from django_filters import rest_framework as filters


class AbandonedObjectListCreateAPIView(generics.ListCreateAPIView):
    queryset = get_all_objects()
    serializer_class = AbandonedObjectSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AbandonedObjectFilter

    def get_queryset(self):
        return get_available_objects_for_user(self.request.user)


class AbandonedObjectRetrieveAPIView(generics.RetrieveAPIView):
    queryset = get_all_objects()
    serializer_class = AbandonedObjectSerializer


class AbandonedObjectCategoryListAPIView(generics.ListAPIView):
    queryset = get_all_categories()
    serializer_class = AbandonedObjectCategorySerializer
    filter_backends = (filters.DjangoFilterBackend,)
