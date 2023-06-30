import aiogram
from conf import settings
from enum import Enum
from utils import events, cls_utils
from .models import TelegramUser, Language
from .sender import Sender


class UIObject(events.EventChannel, metaclass=cls_utils.SingletonMeta):
    class Meta:
        autoshow = False
        autohide = False

    class Event:
        INITIALIZE = 1
        DESTROY = 2
        SHOW = 3
        HIDE = 4
        ATTACH = 5
        DETACH = 6

    def __init__(self, bot: aiogram.Bot = None):
        self._aiogram_bot = bot
        self.sender = cls_utils.get_class(settings.BOT.SENDER_CLASS, not settings.DEBUG, Sender)()
        self._visible = False
        super(UIObject, self).__init__()

    @classmethod
    def set_parent_view(cls, view):
        cls._view = view

    @classmethod
    @property
    def parent_view(cls):
        return getattr(cls, '_view', None)

    async def show(self, user: TelegramUser):
        await self.async_publish(self.Event.SHOW, user)
        self._visible = True

    async def hide(self, user: TelegramUser):
        await self.async_publish(self.Event.HIDE, user)
        self._visible = False

    def is_visible(self) -> bool:
        return self._visible

    @property
    def visible(self) -> bool:
        return self._visible
