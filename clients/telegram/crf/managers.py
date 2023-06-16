from crf.serializers import Serializer


class APIManager:
    class Meta:
        serializer_class: type[Serializer]

    @classmethod
    def get_serializer(cls) -> type[Serializer]:
        try:
            return cls.Meta.serializer_class
        except AttributeError:
            raise AttributeError('Serializer class not specified')

    @classmethod
    def create(cls, **data):
        serializer = cls.get_serializer()
        instance = serializer.deserialize(data)

        return instance

    @classmethod
    def retrieve(cls):
        pass

    @classmethod
    def update(cls):
        pass

    @classmethod
    def destroy(cls):
        pass

    @classmethod
    def list(cls):
        pass
