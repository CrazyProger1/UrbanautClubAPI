import functools
import aiogram

from enum import Enum
from typing import Optional, Callable
from aiogram import types
from utils import cls_utils, string, events
from .ui import UIObject
from .models import TelegramUser, Language
from .keyboards import Keyboard


class View(events.EventChannel, metaclass=cls_utils.SingletonMeta):
    keyboard_classes: tuple[type[Keyboard]] = (

    )

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
        self._attached_objects: list[UIObject] = []

        super(View, self).__init__()
        self._attach_keyboards()

    def _attach_keyboards(self):
        for keyboard in self.keyboard_classes:
            self.attach(keyboard(self._aiogram_bot))

    async def _initialize_objects(self, user: TelegramUser):
        for obj in self._attached_objects:
            await obj.initialize(user)

    async def _destroy_objects(self, user: TelegramUser):
        for obj in self._attached_objects:
            await obj.destroy(user)

    async def _show_objects(self, user: TelegramUser):
        for obj in self._attached_objects:
            if getattr(obj.Meta, 'autoshow', False):
                await obj.show(user)

    async def _hide_objects(self, user: TelegramUser):
        for obj in self._attached_objects:
            if getattr(obj.Meta, 'autohide', False):
                await obj.hide(user)

    def get_attached(self) -> tuple[UIObject]:
        return tuple(self._attached_objects)

    def attach(self, obj: UIObject):
        if obj not in self._attached_objects:
            self._attached_objects.append(obj)

    def detach(self, obj: UIObject):
        if obj in self._attached_objects:
            self._attached_objects.remove(obj)

    async def back(self, user: TelegramUser):
        try:
            prev_page, _ = self.Meta.path.rsplit('.', 1)
            await self._set_view(user, prev_page)
        except ValueError:
            pass

    async def next(self, user: TelegramUser, view: any):
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

    async def initialize(self, user: TelegramUser):
        await self.async_publish(self.Event.INITIALIZE, user)
        await self._initialize_objects(user)
        await self._show_objects(user)

    async def destroy(self, user: TelegramUser):
        await self.async_publish(self.Event.DESTROY, user)
        await self._hide_objects(user)

    async def handle_callback(self, *args, **kwargs):
        await self.async_publish(self.Event.CALLBACK, *args, **kwargs)

    async def handle_message(self, *args, **kwargs):
        await self.async_publish(self.Event.MESSAGE, *args, **kwargs)

    async def handle_media(self, *args, **kwargs):
        await self.async_publish(self.Event.MEDIA, *args, **kwargs)

    async def handle_command(self, *args, **kwargs):
        await self.async_publish(self.Event.COMMAND, *args, **kwargs)
