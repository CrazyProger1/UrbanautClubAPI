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

    def __init__(self, bot: aiogram.Bot = None):
        self._aiogram_bot = bot
        self._page = None
        self.sender = cls_utils.get_class(settings.BOT.SENDER_CLASS, not settings.DEBUG, Sender)()
        super(Task, self).__init__()

    def bind_parent_page(self, page):
        self._page = page

    @property
    def parent_page(self):
        return getattr(self, '_page', None)

    @property
    def bot(self) -> aiogram.Bot:
        return self._aiogram_bot

    async def execute(self, user: TelegramUser):
        await self.async_publish(self.Event.EXECUTE, user=user)
        await self.async_publish(self.Event.DONE, user=user)

    async def cancel(self, user: TelegramUser):
        await self.async_publish(self.Event.CANCEL, user=user)
