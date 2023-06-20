import aiogram

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
        self._sender = Sender()
        self._view = None
        super(UIObject, self).__init__()

    def set_parent_view(self, view):
        self._view = view

    async def show(self, user: TelegramUser):
        await self.async_publish(self.Event.SHOW, user)

    async def hide(self, user: TelegramUser):
        await self.async_publish(self.Event.HIDE, user)
