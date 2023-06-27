from database.model import Model
from playhouse import shortcuts
from utils import cls_utils
from crf.fields import *


class SerializerMeta(cls_utils.MetaChecker):
    _default_values = {
        'fields': '__all__'
    }
    _required_meta_fields = (
        'model',
    )


class Serializer(metaclass=SerializerMeta):
    class Meta:
        model: type[Model] = None
        fields = '__all__'

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

        fields = model.__dict__.keys() if cls.Meta.fields == '__all__' else cls.Meta.fields

        data_keys = tuple(data.keys())
        for key in data_keys:
            if key not in fields:
                data.pop(key, None)

        for field in dir(cls):

            val = getattr(cls, field)
            if isinstance(val, MethodField):
                setter = getattr(cls, val.setter, None)
                if setter:
                    setter(data)

        return shortcuts.dict_to_model(model, data)
