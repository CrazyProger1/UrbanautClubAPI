from crf import APIManager, APIRoute
from serializers import AbandonedObjectSerializer


class AbandonedObjectAPIManager(APIManager):
    class Meta:
        serializer_class = AbandonedObjectSerializer
        routes = {
            APIRoute.COMMON: 'http://127.0.0.1:8000/api/v1/objects/'
        }
