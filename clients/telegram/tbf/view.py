import functools
import aiogram

from enum import Enum
from typing import Optional, Callable
from aiogram import types
from utils import cls_utils, string, events


class View(events.EventChannel, metaclass=cls_utils.SingletonMeta):
    class Meta:
        default = False
        path = ''

    class Event(Enum):
        INITIALIZE = 1
        DESTROY = 2
        MESSAGE = 3
        COMMAND = 4
        CALLBACK = 5
        MEDIA = 6

    def __init__(self, bot: aiogram.Bot, set_view_callback: Callable):
        self._aiogram_bot = bot
        self._set_view = set_view_callback
        super(View, self).__init__()

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
        await self.async_publish(self.Event.INITIALIZE, user)

    async def destroy(self, user):
        await self.async_publish(self.Event.DESTROY, user)

    async def handle_callback(self, *args, **kwargs):
        await self.async_publish(self.Event.CALLBACK, args, kwargs)

    async def handle_message(self, *args, **kwargs):
        await self.async_publish(self.Event.MESSAGE, args, kwargs)

    async def handle_media(self, *args, **kwargs):
        await self.async_publish(self.Event.MEDIA, args, kwargs)

    async def handle_command(self, *args, **kwargs):
        await self.async_publish(self.Event.COMMAND, args, kwargs)
