import aiogram

from enum import Enum
from utils import events, cls_utils
from .models import TelegramUser, Language


class UIObject(events.EventChannel, metaclass=cls_utils.SingletonMeta):
    class Meta:
        autoshow = False
        autohide = False

    class Event:
        INITIALIZE = 1
        DESTROY = 2
        SHOW = 3
        HIDE = 4

    def __init__(self, bot: aiogram.Bot):
        self._aiogram_bot = bot
        super(UIObject, self).__init__()

    async def initialize(self, user: TelegramUser):
        await self.async_publish(self.Event.INITIALIZE, user)

    async def destroy(self, user: TelegramUser):
        await self.async_publish(self.Event.DESTROY, user)

    async def show(self, user: TelegramUser):
        await self.async_publish(self.Event.SHOW, user)

    async def hide(self, user: TelegramUser):
        await self.async_publish(self.Event.HIDE, user)
