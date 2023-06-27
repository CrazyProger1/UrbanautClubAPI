from typing import Generator
from utils.import_utils import import_module


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Customizable:
    cls_path: str = None

    def __new__(cls, *args, **kwargs):
        if cls in Customizable.__subclasses__() and cls.cls_path and cls.__name__ != cls.cls_path.rsplit('.', 1)[-1]:
            subclass = import_module(cls.cls_path)
            if issubclass(subclass, Customizable):
                return subclass(*args, **kwargs)
            else:
                raise  #

        new_instance = super(Customizable, cls).__new__(cls, *args, **kwargs)
        return new_instance


class MetaChecker(type):
    _default_values: dict = {}
    _required_meta_fields: list | tuple = []

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)

        try:
            meta = cls.Meta
        except AttributeError:
            raise AttributeError(f'{cls.__name__}.Meta not specified')

        for field, value in mcs._default_values.items():
            setattr(meta, field, getattr(meta, field, value))

        for field in mcs._required_meta_fields:
            if not hasattr(meta, field):
                raise AttributeError(f'{cls.__name__}.Meta.{field} not specified')

        return cls


def iter_subclasses(cls, max_level=-1) -> Generator:
    if max_level == 0:
        return

    for subcls in cls.__subclasses__():
        yield subcls
        for subsubcls in iter_subclasses(subcls, max_level - 1):
            yield subsubcls
