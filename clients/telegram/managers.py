from crf import APIManager
from serializers import AbandonedObjectSerializer


class AbandonedObjectAPIManager(APIManager):
    class Meta:
        serializer_class = AbandonedObjectSerializer
