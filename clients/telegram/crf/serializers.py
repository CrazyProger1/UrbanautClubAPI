from crf.models import Model
from playhouse import shortcuts


class Serializer:
    class Meta:
        model: type[Model]

    @classmethod
    def get_model(cls) -> type[Model]:
        try:
            model = cls.Meta.model
            if not issubclass(model, Model):
                raise TypeError('Meta.model must be a subclass of Model')
            return model
        except AttributeError:
            raise AttributeError('Meta.model not specified')

    @classmethod
    def serialize(cls, instance: Model) -> dict:
        return shortcuts.model_to_dict(instance)

    @classmethod
    def deserialize(cls, data: dict) -> Model:
        model = cls.get_model()
        return shortcuts.dict_to_model(model, data)
