import peewee

from .database import connection


class Model(peewee.Model):
    __instances = {}

    class Meta:
        database = connection

    def __new__(cls, *args, **kwargs):
        pk_field = cls._meta.primary_key.name
        pk_val = kwargs.pop(pk_field, None)

        instance = cls.__instances.get(pk_val)
        if instance:
            return instance
        new_instance = super(Model, cls).__new__(cls)
        return new_instance

    def __setattr__(self, key, value):
        pk_field = self._meta.primary_key.name

        if key == pk_field:
            self.__instances.update({value: self})

        super(Model, self).__setattr__(key, value)


