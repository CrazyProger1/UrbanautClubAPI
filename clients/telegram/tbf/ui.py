import aiogram
from conf import settings
from enum import Enum
from utils import events, cls_utils
from .models import TelegramUser, Language
from .sender import Sender


class UIObject(events.EventChannel):
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
        self._visible_for = set()
        self._page = None
        super(UIObject, self).__init__()

    @property
    def bot(self) -> aiogram.Bot:
        return self._aiogram_bot

    def bind_parent_page(self, page):
        self._page = page

    @property
    def parent_page(self):
        return getattr(self, '_page', None)

    async def show(self, user: TelegramUser):
        await self.async_publish(self.Event.SHOW, user)
        self._visible_for.add(user)

    async def hide(self, user: TelegramUser):
        try:
            self._visible_for.remove(user)
            await self.async_publish(self.Event.HIDE, user)
        except KeyError:
            pass

    def is_visible(self, user: TelegramUser) -> bool:
        return user in self._visible_for
