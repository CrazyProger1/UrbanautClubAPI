import functools
import inspect

import aiogram

from enum import Enum
from typing import Optional, Callable
from conf import settings
from aiogram import types
from utils import cls_utils, string, events
from .ui import UIObject
from .models import TelegramUser, Language
from .keyboards import Keyboard
from .sender import Sender
from .task import Task


class PageMeta(cls_utils.MetaChecker, cls_utils.SingletonMeta):
    _default_values = {
        'default': False
    }
    _required_meta_fields = (
        'path',
    )


class Page(events.EventChannel, metaclass=PageMeta):
    object_classes: tuple[type[UIObject]] = (

    )

    task_classes: tuple[type[Task]] = (

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

    def __init__(self, bot: aiogram.Bot = None, set_page_callback: Callable = None):
        self._aiogram_bot = bot
        self.sender = cls_utils.get_class(settings.BOT.SENDER_CLASS, not settings.DEBUG, Sender)()
        self._set_page = set_page_callback
        self._tasks = []
        self._objects = []

        super(Page, self).__init__()

        self._initialize_objects()
        self._initialize_tasks()
        self._subscribe_on_events()

    def _initialize_tasks(self):
        for task_cls in self.task_classes:
            if not inspect.isclass(task_cls) or not issubclass(task_cls, Task):
                raise
            task = task_cls(bot=self._aiogram_bot, parent_page=self)
            self._tasks.append(task)

    def _initialize_objects(self):
        for obj_cls in self.object_classes:
            if not inspect.isclass(obj_cls) or not issubclass(obj_cls, UIObject):
                raise
            obj = obj_cls(bot=self._aiogram_bot, parent_page=self)
            self._objects.append(obj)

    def _subscribe_on_events(self):
        self.subscribe(self.Event.INITIALIZE, self._initialize_page)
        self.subscribe(self.Event.DESTROY, self._destroy_page)

        self.subscribe(self.Event.INITIALIZE, self.on_initialize)
        self.subscribe(self.Event.DESTROY, self.on_destroy)
        self.subscribe(self.Event.MEDIA, self.on_media)
        self.subscribe(self.Event.MESSAGE, self.on_message)
        self.subscribe(self.Event.CALLBACK, self.on_callback)
        self.subscribe(self.Event.COMMAND, self.on_command)

        for keyboard in self.get_keyboards():
            keyboard.subscribe(keyboard.Event.BUTTON_PRESSED, self.on_button_pressed)

        for task in self.get_tasks():
            task.subscribe(task.Event.DONE, self.on_task_done)

    @functools.cache
    def get_objects(self) -> tuple[UIObject, ...]:
        return tuple(self._objects)

    @functools.cache
    def get_keyboards(self) -> tuple[Keyboard, ...]:
        return tuple(filter(lambda obj: isinstance(obj, Keyboard), self.get_objects()))

    @functools.cache
    def get_tasks(self) -> tuple[Task, ...]:
        return tuple(self._tasks)

    async def _initialize_page(self, user: TelegramUser):
        for obj in self._objects:
            await obj.async_publish(obj.Event.INITIALIZE, user)
            if getattr(obj.Meta, 'autoshow', False):
                await self.show_object(user=user, obj=obj)

    async def _destroy_page(self, user: TelegramUser):
        for obj in self._objects:
            await obj.async_publish(obj.Event.DESTROY, user)
            if getattr(obj.Meta, 'autohide', False):
                await self.hide_object(user=user, obj=obj)

    async def execute_task(self, user: TelegramUser, task: type[Task]):
        if inspect.isclass(task) and issubclass(task, Task):
            task = task()

        if task in self._tasks:
            await task.async_publish(task.Event.EXECUTE, user=user)

    async def cancel_task(self, user: TelegramUser, task: type[Task] | Task):
        if inspect.isclass(task) and issubclass(task, Task):
            task = task()

        if task in self._tasks:
            await task.async_publish(task.Event.CANCEL, user=user)

    async def show_object(self, user: TelegramUser, obj: type[UIObject] | UIObject):
        if inspect.isclass(obj) and issubclass(obj, UIObject):
            obj = obj()

        if obj in self._objects:
            await obj.async_publish(obj.Event.SHOW, user=user)

    async def hide_object(self, user: TelegramUser, obj: type[UIObject] | UIObject):
        if inspect.isclass(obj) and issubclass(obj, UIObject):
            obj = obj()

        if obj in self._objects:
            await obj.async_publish(obj.Event.HIDE, user=user)

    async def back(self, user: TelegramUser):
        try:
            prev_page, _ = self.Meta.path.rsplit('.', 1)
            await self._set_page(user, prev_page)
        except ValueError:
            pass

    async def next(self, user: TelegramUser, page: any):
        if isinstance(page, str):
            try:
                await self._set_page(
                    user,
                    string.join_by(self._set_page, page)
                )
            except ValueError:
                await self._set_page(
                    user,
                    string.join_by(page)
                )
            return
        await self._set_page(
            user,
            page
        )

    @classmethod
    @functools.cache
    def get_default(cls) -> Optional["Page"]:
        for page in cls_utils.iter_subclasses(cls):
            if page.Meta.default:
                return page()

    @classmethod
    @functools.cache
    def get(cls, path: str) -> Optional["Page"]:
        for page in cls_utils.iter_subclasses(cls):
            if page.Meta.path == path:
                return page()

    async def on_initialize(self, user: TelegramUser):
        pass

    async def on_destroy(self, user: TelegramUser):
        pass

    async def on_message(self, *args, **kwargs):
        pass

    async def on_command(self, *args, **kwargs):
        pass

    async def on_media(self, *args, **kwargs):
        pass

    async def on_callback(self, *args, **kwargs):
        pass

    async def on_button_pressed(self, keyboard: Keyboard, button: str, user: TelegramUser, **kwargs):
        pass

    async def on_task_done(self, task: Task, user: TelegramUser):
        pass

    def __repr__(self):
        return f'Page<{self.Meta.path}>'
