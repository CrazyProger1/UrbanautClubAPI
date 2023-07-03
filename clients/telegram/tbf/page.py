import functools
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
    keyboard_classes: tuple[type[Keyboard]] = (

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
        self._tasks = [task_cls(bot=self._aiogram_bot) for task_cls in self.task_classes]
        self._attached_objects: list[UIObject] = []

        super(Page, self).__init__()

        self._attach_keyboards()
        self._subscribe_on_events()
        self._initialize_tasks()

    def _subscribe_on_events(self):
        self.subscribe(self.Event.INITIALIZE, self._initialize)
        self.subscribe(self.Event.DESTROY, self._destroy)

    def _initialize_tasks(self):
        for task in self._tasks:
            task.bind_parent_page(self)

    async def _initialize(self, user: TelegramUser):
        await self._initialize_objects(user)
        await self._show_objects(user)

    async def _destroy(self, user: TelegramUser):
        await self._hide_objects(user)

    def _attach_keyboards(self):
        for keyboard in self.keyboard_classes:
            self.attach(keyboard(self._aiogram_bot))

    async def _initialize_objects(self, user: TelegramUser):
        for obj in self._attached_objects:
            await obj.async_publish(obj.Event.INITIALIZE, user)

    async def _destroy_objects(self, user: TelegramUser):
        for obj in self._attached_objects:
            await obj.async_publish(obj.Event.DESTROY, user)

    async def _show_objects(self, user: TelegramUser):
        for obj in self._attached_objects:
            if getattr(obj.Meta, 'autoshow', False):
                await obj.show(user)

    async def _hide_objects(self, user: TelegramUser):
        for obj in self._attached_objects:
            if getattr(obj.Meta, 'autohide', False):
                await obj.hide(user)

    async def execute_task(self, user: TelegramUser, task: type[Task]):
        if issubclass(task, Task):
            task = task()

        if task in self._tasks:
            await task.execute(user=user)

    async def cancel_task(self, user: TelegramUser, task: type[Task] | Task):
        if issubclass(task, Task):
            task = task()

        if task in self._tasks:
            await task.cancel(user=user)

    async def show_object(self, user: TelegramUser, obj: type[UIObject] | UIObject):
        if issubclass(obj, UIObject):
            obj = obj()

        if obj in self._attached_objects:
            await obj.show(user=user)

    async def hide_object(self, user: TelegramUser, obj: type[UIObject]):
        if issubclass(obj, UIObject):
            obj = obj()

        if obj in self._attached_objects:
            await obj.hide(user=user)

    def get_attached(self) -> tuple[UIObject]:
        return tuple(self._attached_objects)

    def attach(self, obj: UIObject):
        if obj not in self._attached_objects:
            obj.bind_parent_page(self)
            obj.publish(obj.Event.ATTACH)
            self._attached_objects.append(obj)

    def detach(self, obj: UIObject):
        if obj in self._attached_objects:
            obj.publish(obj.Event.DETACH)
            self._attached_objects.remove(obj)

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
