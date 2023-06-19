import functools
import aiogram

from typing import Optional, Callable
from aiogram import types
from utils import cls_utils, string


class View(metaclass=cls_utils.SingletonMeta):
    class Meta:
        default = False
        path = ''

    def __init__(self, bot: aiogram.Bot, set_view_callback: Callable):
        self._aiogram_bot = bot
        self._set_view = set_view_callback

    async def back(self, user):
        try:
            prev_page, _ = self.Meta.path.rsplit('.', 1)
            await self._set_view(user, prev_page)
        except ValueError:
            pass

    async def next(self, user, view: any):
        if isinstance(view, str):
            try:
                await self._set_view(
                    user,
                    string.join_by(self._set_view, view)
                )
            except ValueError:
                await self._set_view(
                    user,
                    string.join_by(view)
                )
            return
        await self._set_view(
            user,
            view
        )

    @classmethod
    @functools.cache
    def get_default(cls) -> Optional["View"]:
        for view in cls_utils.iter_subclasses(cls):
            if view.Meta.default:
                return view()

    @classmethod
    @functools.cache
    def get(cls, path: str) -> Optional["View"]:
        for view in cls_utils.iter_subclasses(cls):
            if view.Meta.path == path:
                return view()

    async def initialize(self, user):
        pass

    async def destroy(self, user):
        pass

    async def handle_callback(self, *args, **kwargs):
        pass

    async def handle_message(self, *args, **kwargs):
        pass

    async def handle_media(self, *args, **kwargs):
        pass

    async def handle_command(self, *args, **kwargs):
        pass
