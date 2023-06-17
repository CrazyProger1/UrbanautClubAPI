import functools

from typing import Optional

from utils import cls_utils


class View(metaclass=cls_utils.SingletonMeta):
    class Meta:
        default = False
        path = ''

    @classmethod
    @functools.cache
    def get_default(cls) -> Optional["View"]:
        for view in cls_utils.iter_subclasses(cls):
            if view.Meta.default:
                return view()

    async def initialize(self):
        pass

    async def destroy(self):
        pass

    async def handle_callback(self, *args, **kwargs):
        pass

    async def handle_message(self, *args, **kwargs):
        pass

    async def handle_media(self, *args, **kwargs):
        pass

    async def handle_command(self, *args, **kwargs):
        pass
