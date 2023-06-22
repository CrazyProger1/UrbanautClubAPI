from crf.manager import APIManager, APIRoute
from app.serializers import *


class AbandonedObjectAPIManager(APIManager):
    class Meta:
        serializer_class = AbandonedObjectSerializer
        routes = {
            APIRoute.COMMON: 'http://127.0.0.1:8000/api/v1/objects/'
        }


class AbandonedObjectCategoryAPIManager(APIManager):
    class Meta:
        serializer_class = AbandonedObjectCategorySerializer
        routes = {
            APIRoute.COMMON: 'http://127.0.0.1:8000/api/v1/objects/categories/'
        }
