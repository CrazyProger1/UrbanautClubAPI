import aiogram
from conf import settings
from enum import Enum
from utils import events, cls_utils
from .models import TelegramUser, Language
from .sender import Sender


class TaskMeta(cls_utils.MetaChecker, cls_utils.SingletonMeta):
    _default_values: dict = {}
    _required_meta_fields: list | tuple = []


class Task(events.EventChannel, metaclass=TaskMeta):
    class Meta:
        pass

    class Event(Enum):
        EXECUTE = 1
        DONE = 2
        CANCEL = 3

    def __init__(self, bot: aiogram.Bot = None, parent_page=None):
        self._aiogram_bot = bot
        self._parent_page = parent_page
        self.sender = cls_utils.get_class(settings.BOT.SENDER_CLASS, not settings.DEBUG, Sender)()
        self._executing_for = set()

        super(Task, self).__init__()
        self._subscribe_on_events()

    def _subscribe_on_events(self):
        self.subscribe(self.Event.EXECUTE, self._execute)
        self.subscribe(self.Event.CANCEL, self._cancel)
        self.subscribe(self.Event.DONE, self._done)

        self.subscribe(self.Event.EXECUTE, self.on_execute)
        self.subscribe(self.Event.CANCEL, self.on_cancel)
        self.subscribe(self.Event.DONE, self.on_done)

    async def _execute(self, user: TelegramUser):
        self._executing_for.add(user)

    async def _cancel(self, user: TelegramUser):
        try:
            self._executing_for.remove(user)
        except ValueError:
            pass

    async def _done(self, user: TelegramUser):
        try:
            self._executing_for.remove(user)
        except ValueError:
            pass

    @property
    def page(self):
        return self._parent_page

    @property
    def bot(self) -> aiogram.Bot:
        return self._aiogram_bot

    async def done(self, user: TelegramUser):
        await self.async_publish(self.Event.DONE, user=user)

    def is_executing(self, user: TelegramUser) -> bool:
        return user in self._executing_for

    async def on_execute(self, user: TelegramUser):
        pass

    async def on_cancel(self, user: TelegramUser):
        pass

    async def on_done(self, user: TelegramUser):
        pass
