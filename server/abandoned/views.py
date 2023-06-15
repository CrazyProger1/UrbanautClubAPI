from django.shortcuts import render
from rest_framework import generics
from abandoned.serializers import *
from abandoned.services import *
from abandoned.permissions import *


class AbandonedObjectListAPIView(generics.ListAPIView):
    queryset = get_all_objects()
    serializer_class = AbandonedObjectSerializer

    def get_queryset(self):
        return get_available_objects_for_user(self.request.user)
