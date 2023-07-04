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

    def __init__(self, bot: aiogram.Bot = None, parent_page=None):
        self._aiogram_bot = bot
        self.sender = cls_utils.get_class(settings.BOT.SENDER_CLASS, not settings.DEBUG, Sender)()
        self._visible_for = set()
        self._parent_page = parent_page

        super(UIObject, self).__init__()
        self._subscribe_on_events()

    def _subscribe_on_events(self):
        self.subscribe(self.Event.SHOW, self._show)
        self.subscribe(self.Event.HIDE, self._hide)

        self.subscribe(self.Event.SHOW, self.on_show)
        self.subscribe(self.Event.HIDE, self.on_hide)

    @property
    def bot(self) -> aiogram.Bot:
        return self._aiogram_bot

    @property
    def page(self):
        return self._parent_page

    async def _show(self, user: TelegramUser):
        self._visible_for.add(user)

    async def _hide(self, user: TelegramUser):
        try:
            self._visible_for.remove(user)
        except KeyError:
            pass

    async def on_show(self, user: TelegramUser):
        pass

    async def on_hide(self, user: TelegramUser):
        pass

    def is_visible(self, user: TelegramUser) -> bool:
        return user in self._visible_for
