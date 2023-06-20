import aiogram

from enum import Enum
from utils import events, cls_utils
from .models import TelegramUser, Language


class UIObject(events.EventChannel, metaclass=cls_utils.SingletonMeta):
    class Event:
        INITIALIZE = 1
        DESTROY = 2

    def __init__(self, bot: aiogram.Bot):
        self._aiogram_bot = bot
        super(UIObject, self).__init__()

    async def initialize(self, user: TelegramUser):
        await self.async_publish(self.Event.INITIALIZE, user)

    async def destroy(self, user: TelegramUser):
        await self.async_publish(self.Event.DESTROY, user)
